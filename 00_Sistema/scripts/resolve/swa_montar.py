"""DaVinci Resolve: monta la lección a partir del plan de edición.

Pasos: proyecto -> Media Pool -> timeline solo con tramos de voz (Auto-Cut) ->
punch-in alterno -> B-Roll/imágenes en V2 y audios en A2 -> marcadores.

Se lanza desde Workspace > Scripts > Edit > "SWA 1 - Montar leccion".
Antes, en la terminal: python builder.py editar M01 L01
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swa_comun import cargar_plan, fps_valido, log, obtener_resolve  # noqa: E402


def item_por_ruta(media_pool, carpeta, ruta):
    """Reutiliza el clip si ya está en el Media Pool (re-ejecutar no duplica)."""
    objetivo = os.path.normcase(os.path.abspath(ruta))
    for clip in carpeta.GetClipList() or []:
        if os.path.normcase(os.path.abspath(clip.GetClipProperty("File Path") or "")) == objetivo:
            return clip
    importados = media_pool.ImportMedia([ruta])
    if not importados:
        raise RuntimeError("No se pudo importar: " + ruta)
    return importados[0]


def frames_de_clip(clip, fps):
    try:
        return int(clip.GetClipProperty("Frames"))
    except (TypeError, ValueError):
        return int(5 * fps)


def main(g):
    plan = cargar_plan()
    resolve = obtener_resolve(g)
    pm = resolve.GetProjectManager()

    # 1. Proyecto (se crea una vez; si existe se reutiliza)
    proyecto = pm.LoadProject(plan["proyecto"]) or pm.CreateProject(plan["proyecto"])
    if not proyecto:
        raise SystemExit("No pude abrir ni crear el proyecto " + plan["proyecto"])
    fps = float(plan["fps"])
    if not proyecto.GetTimelineCount():
        # Solo se puede fijar antes de crear el primer timeline.
        proyecto.SetSetting("timelineFrameRate", fps_valido(fps))
        proyecto.SetSetting("timelineResolutionWidth", "1920")
        proyecto.SetSetting("timelineResolutionHeight", "1080")
    log("Proyecto: " + plan["proyecto"])

    # 2. Media Pool
    mp = proyecto.GetMediaPool()
    raiz = mp.GetRootFolder()
    mp.SetCurrentFolder(raiz)
    raw = item_por_ruta(mp, raiz, plan["raw"])
    fps_clip = float(raw.GetClipProperty("FPS") or fps)
    assets = {}
    for ins in plan["inserciones"]:
        if ins["archivo"] not in assets:
            assets[ins["archivo"]] = item_por_ruta(mp, raiz, ins["archivo"])
    log("Media Pool: RAW + %d assets" % len(assets))

    # 3. Timeline nuevo con solo los tramos de voz (= cortes + ripple delete)
    nombre = plan["base"]
    n = 1
    existentes = {proyecto.GetTimelineByIndex(i + 1).GetName() for i in range(proyecto.GetTimelineCount())}
    while nombre in existentes:
        n += 1
        nombre = "%s_v%d" % (plan["base"], n)
    timeline = mp.CreateEmptyTimeline(nombre)
    proyecto.SetCurrentTimeline(timeline)
    clips = [{"mediaPoolItem": raw, "startFrame": int(round(a * fps_clip)), "endFrame": int(round(b * fps_clip))}
             for a, b in plan["segmentos"]]
    mp.AppendToTimeline(clips)
    log("Auto-Cut: %d tramos, %.1f s -> %.1f s" % (len(clips), plan["duracion_raw_s"], plan["duracion_final_s"]))

    # 4. Punch-in alterno: disimula los jump-cuts sin parecer aleatorio
    zoom = float(plan.get("zoom_punch_in") or 1.0)
    if zoom > 1.0:
        for i, item in enumerate(timeline.GetItemListInTrack("video", 1) or []):
            if i % 2 == 1:
                item.SetProperty("ZoomX", zoom)
                item.SetProperty("ZoomY", zoom)

    # 5. Pistas V2 / A2 y assets sincronizados con el texto
    while timeline.GetTrackCount("video") < 2:
        timeline.AddTrack("video")
    while timeline.GetTrackCount("audio") < 2:
        timeline.AddTrack("audio", "stereo")
    inicio_tl = timeline.GetStartFrame()
    fps_tl = float(proyecto.GetSetting("timelineFrameRate") or fps)
    fin_pista = {"V2": 0, "A2": 0}
    for ins in plan["inserciones"]:
        clip = assets[ins["archivo"]]
        es_audio = ins["pista"] == "A2"
        if ins["duracion_s"]:
            dur = int(round(ins["duracion_s"] * fps_tl))
        else:
            dur = frames_de_clip(clip, fps_tl)
        offset = max(int(round(ins["inicio_s"] * fps_tl)), fin_pista[ins["pista"]])  # sin solapes
        resultado = mp.AppendToTimeline([{
            "mediaPoolItem": clip, "startFrame": 0, "endFrame": dur - 1,
            "trackIndex": 2, "recordFrame": inicio_tl + offset,
            "mediaType": 2 if es_audio else 1,   # el B-Roll entra sin su audio
        }])
        if resultado:
            fin_pista[ins["pista"]] = offset + dur
        else:
            log("AVISO: no se pudo insertar " + os.path.basename(ins["archivo"]))

    # 6. Marcadores: indicaciones de PANTALLA, notas y assets que faltan
    for m in plan["marcadores"]:
        timeline.AddMarker(int(round(m["inicio_s"] * fps_tl)), m["color"], m["nombre"], m["nota"], 1, "")

    log("Listo: timeline '%s'. Revisa los marcadores y lanza 'SWA 2 - Render'." % nombre)
    log("Sincronización: " + plan["metodo_sincronizacion"])


main(globals())

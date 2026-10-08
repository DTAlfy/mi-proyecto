"""DaVinci Resolve: monta la lección a partir del plan de edición.

Pasos: proyecto -> Media Pool -> timeline solo con tramos de voz (Auto-Cut) y
tarjetas "Escucha" donde suena cada [AUDIO] -> punch-in alterno -> visuales en V2,
audios en A2 -> marcadores.

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
    secuencia = plan.get("secuencia") or [{"tipo": "raw", "inicio_s": a, "fin_s": b} for a, b in plan["segmentos"]]
    assets = {}
    rutas = [ins["archivo"] for ins in plan["inserciones"]]
    for ev in secuencia:
        if ev["tipo"] == "pausa":
            rutas += [ev["imagen"], ev["audio"]]
    for ruta in rutas:
        if ruta not in assets:
            assets[ruta] = item_por_ruta(mp, raiz, ruta)
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
    clips = []
    for ev in secuencia:
        if ev["tipo"] == "raw":
            clips.append({"mediaPoolItem": raw, "startFrame": int(round(ev["inicio_s"] * fps_clip)),
                          "endFrame": int(round(ev["fin_s"] * fps_clip))})
        else:  # tarjeta "Escucha" fija mientras suena el audio
            clips.append({"mediaPoolItem": assets[ev["imagen"]], "startFrame": 0,
                          "endFrame": int(round(ev["duracion_s"] * fps)) - 1})
    mp.AppendToTimeline(clips)
    n_pausas = sum(1 for ev in secuencia if ev["tipo"] == "pausa")
    log("Auto-Cut: %d tramos + %d pausas de audio, %.1f s -> %.1f s"
        % (len(clips) - n_pausas, n_pausas, plan["duracion_raw_s"], plan["duracion_final_s"]))

    # 4. Punch-in alterno (solo tramos de voz): disimula los jump-cuts sin parecer aleatorio
    v1 = timeline.GetItemListInTrack("video", 1) or []
    alineado = len(v1) == len(secuencia)
    zoom = float(plan.get("zoom_punch_in") or 1.0)
    n_raw = 0
    for ev, item in zip(secuencia, v1):
        if ev["tipo"] == "raw":
            if zoom > 1.0 and n_raw % 2 == 1:
                item.SetProperty("ZoomX", zoom)
                item.SetProperty("ZoomY", zoom)
            n_raw += 1

    # 5. Pistas V2 / A2 y assets sincronizados con el texto
    while timeline.GetTrackCount("video") < 2:
        timeline.AddTrack("video")
    while timeline.GetTrackCount("audio") < 2:
        timeline.AddTrack("audio", "stereo")
    inicio_tl = timeline.GetStartFrame()
    fps_tl = float(proyecto.GetSetting("timelineFrameRate") or fps)

    # Audios de las pausas en A2, alineados con su tarjeta "Escucha" real en V1
    t_final = 0.0
    for i, ev in enumerate(secuencia):
        if ev["tipo"] == "pausa":
            record = v1[i].GetStart() if alineado else inicio_tl + int(round(t_final * fps_tl))
            mp.AppendToTimeline([{"mediaPoolItem": assets[ev["audio"]], "startFrame": 0,
                                  "endFrame": frames_de_clip(assets[ev["audio"]], fps_tl) - 1,
                                  "trackIndex": 2, "recordFrame": record, "mediaType": 2}])
        t_final += ev["duracion_s"] if ev["tipo"] == "pausa" else ev["fin_s"] - ev["inicio_s"]

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

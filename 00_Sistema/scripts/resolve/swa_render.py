"""DaVinci Resolve: añade el timeline actual a la cola de render y lo exporta.

Se lanza desde Workspace > Scripts > Edit > "SWA 2 - Render", DESPUÉS de revisar
el montaje. Exporta a 05_Renders_Finales/M01_L01_Clave_FINAL.mp4
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swa_comun import cargar_plan, log, obtener_resolve  # noqa: E402


def main(g):
    plan = cargar_plan()
    resolve = obtener_resolve(g)
    proyecto = resolve.GetProjectManager().GetCurrentProject()
    if not proyecto or proyecto.GetName() != plan["proyecto"]:
        raise SystemExit("Abre el proyecto %s antes de renderizar." % plan["proyecto"])
    timeline = proyecto.GetCurrentTimeline()
    if not timeline:
        raise SystemExit("No hay timeline activo.")

    render = plan["render"]
    if not proyecto.LoadRenderPreset(render["preset"]):
        disponibles = ", ".join(proyecto.GetRenderPresetList() or [])
        raise SystemExit("Preset '%s' no encontrado. Disponibles: %s" % (render["preset"], disponibles))

    os.makedirs(render["carpeta"], exist_ok=True)
    proyecto.SetRenderSettings({
        "SelectAllFrames": True,
        "TargetDir": render["carpeta"],
        "CustomName": os.path.splitext(render["nombre"])[0],
    })
    job = proyecto.AddRenderJob()
    if not job:
        raise SystemExit("No se pudo añadir el trabajo a la cola de render.")
    proyecto.StartRendering(job)
    log("Renderizando '%s' -> %s" % (timeline.GetName(), os.path.join(render["carpeta"], render["nombre"])))


main(globals())

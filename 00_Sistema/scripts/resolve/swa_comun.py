"""Utilidades compartidas por los scripts de DaVinci Resolve (solo librería estándar).

Funciona en DaVinci Resolve GRATIS: los scripts se lanzan desde
Workspace > Scripts > Edit, donde Resolve inyecta `resolve` / `app` / `bmd`.
En Resolve Studio también funcionan desde una terminal externa.
"""

import json
import os

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
# FPS que acepta el ajuste timelineFrameRate de Resolve.
FPS_VALIDOS = ["23.976", "24", "25", "29.97", "30", "47.952", "48", "50", "59.94", "60"]


def obtener_resolve(g):
    """Encuentra el objeto Resolve sea cual sea la forma en que se lanzó el script."""
    if g.get("resolve"):
        return g["resolve"]
    app = g.get("app")
    if app is not None:
        try:
            r = app.GetResolve()
            if r:
                return r
        except Exception:
            pass
    bmd = g.get("bmd")
    if bmd is not None:
        r = bmd.scriptapp("Resolve")
        if r:
            return r
    try:  # Resolve Studio desde terminal externa
        import DaVinciResolveScript as dvr  # noqa: N813
        r = dvr.scriptapp("Resolve")
        if r:
            return r
    except ImportError:
        pass
    raise SystemExit(
        "No encuentro DaVinci Resolve. Abre Resolve y lanza este script desde "
        "Workspace > Scripts (versión gratis) o activa External Scripting (Studio)."
    )


def cargar_plan():
    puntero = os.path.join(RAIZ, "00_Sistema", "ediciones", "ACTUAL.json")
    if not os.path.exists(puntero):
        raise SystemExit("No hay plan de edición. Ejecuta antes: python builder.py editar M01 L01")
    with open(puntero, encoding="utf-8") as f:
        ruta = json.load(f)["plan"]
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def fps_valido(fps):
    return min(FPS_VALIDOS, key=lambda v: abs(float(v) - fps))


def log(msg):
    print("[SWA] " + msg)

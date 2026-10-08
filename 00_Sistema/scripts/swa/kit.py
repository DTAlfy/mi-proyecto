"""Kit de grabación: teleprompter HTML + checklist para el día de grabar.

El objetivo es que el día de grabación SOLO tengas que leer: todo lo que vas a
enseñar en pantalla está listado, generado y nombrado de antemano.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

import markdown

from .assets import ItemPlan
from .config import Config, RAIZ
from .guion import PATRON_ETIQUETA, Guion
from .naming import Leccion

ICONOS = {
    "BROLL": ("🎬", "B-Roll"), "IMG": ("🖼", "Imagen"), "AUDIO": ("🔊", "Audio"),
    "SLIDE": ("📊", "Slide"), "ROADMAP": ("🗺", "Roadmap"), "PANTALLA": ("🖥", "Muestra"),
    "NOTA": ("✏️", "Nota"), "TAREA": ("📘", "Tarea"), "RECURSO": ("📎", "Recurso"),
}
_RE_BLOQUE = re.compile(r"\[(TAREA|RECURSO)(?::\s*([^\]]*))?\](.*?)\[/\1\]", re.S)


def _chip(tipo: str, valor: str) -> str:
    icono, nombre = ICONOS.get(tipo, ("•", tipo))
    texto = f"{nombre}: {valor}" if valor else nombre
    return f'<span class="cue cue-{tipo.lower()}">{icono} {html.escape(texto)}</span>'


def cuerpo_teleprompter(g: Guion) -> str:
    """Markdown del guion -> HTML con las etiquetas convertidas en avisos visuales."""
    texto = _RE_BLOQUE.sub(lambda m: _chip(m[1], (m[2] or "").strip() + " (en el workbook)"), g.cuerpo)
    texto = PATRON_ETIQUETA.sub(lambda m: "" if m["cierre"] else _chip(m["tipo"], (m["valor"] or "").strip()), texto)
    return markdown.markdown(texto)


def teleprompter(g: Guion, lec: Leccion, cfg: Config) -> Path:
    plantilla = (cfg.ruta("plantillas") / "teleprompter.html").read_text(encoding="utf-8")
    pagina = (plantilla
              .replace("{{TITULO}}", html.escape(f"{lec.id} · {lec.titulo}"))
              .replace("{{DURACION}}", f"{g.minutos_estimados:.1f}")
              .replace("{{CUERPO}}", cuerpo_teleprompter(g)))
    destino = cfg.ruta("teleprompter") / lec.archivo("TELEPROMPTER", ".html")
    destino.write_text(pagina, encoding="utf-8")
    return destino


def checklist(g: Guion, lec: Leccion, cfg: Config, plan: list[ItemPlan]) -> Path:
    raw = (cfg.ruta("bruto") / lec.archivo("RAW", ".mp4")).relative_to(RAIZ).as_posix()
    tp = (cfg.ruta("teleprompter") / lec.archivo("TELEPROMPTER", ".html")).relative_to(RAIZ).as_posix()
    lineas = [
        f"# Checklist de grabación — {lec.id} · {lec.titulo}",
        "",
        f"**Objetivo de la lección:** {lec.objetivo}  ",
        f"**Duración estimada de lectura:** {g.minutos_estimados:.1f} min ({len(g.palabras)} palabras)  ",
        f"**Teleprompter:** `{tp}`  ",
        f"**Guarda la grabación como:** `{raw}`",
        "",
        "## Antes de grabar",
        "- [ ] OBS: escena *Clase* (pantalla + cámara), 1920x1080, 30 fps, grabación en MP4 (o MKV con remux automático)",
        "- [ ] OBS: micrófono en la pista de audio 1, picos entre -12 y -6 dB",
        "- [ ] Notificaciones del sistema desactivadas; pestañas no necesarias cerradas",
        "- [ ] Agua, luz frontal y cámara a la altura de los ojos",
        "",
        "## Ten abierto en pantalla (en este orden)",
    ]
    pantallas = g.de_tipo("PANTALLA")
    lineas += [f"{i}. [ ] {e.valor}  _(sección: {e.seccion})_" for i, e in enumerate(pantallas, 1)] or ["- (nada: lección solo a cámara)"]

    lineas += ["", "## Visuales que se insertarán en edición (no hace falta mostrarlos al grabar)"]
    for item in plan:
        ok = "x" if item.destino.exists() else " "
        lineas.append(f"- [{ok}] {item.etiqueta.tipo:<7} `{item.relativo}` — {item.etiqueta.valor or 'roadmap del módulo'}")
    if any(not i.destino.exists() for i in plan):
        lineas += ["", f"> Faltan assets. Ejecuta: `python builder.py assets {lec.modulo:02d} {lec.numero:02d} --generar`"]

    lineas += [
        "",
        "## Al terminar",
        f"- [ ] Mueve/renombra el archivo a `{raw}`",
        f"- [ ] `python builder.py editar {lec.modulo:02d} {lec.numero:02d}` y después en DaVinci: Workspace › Scripts › SWA 1 - Montar leccion",
        "",
        "Consejo: si te equivocas, haz una pausa de 2 segundos, da una palmada y repite la frase entera. El Auto-Cut elimina la pausa; la palmada se ve como un pico en la forma de onda y te indica qué toma borrar al revisar en DaVinci.",
    ]
    destino = cfg.ruta("teleprompter") / lec.archivo("CHECKLIST", ".md")
    destino.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    return destino

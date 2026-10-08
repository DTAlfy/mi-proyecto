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
    "BROLL": ("🎬", "B-Roll"), "IMG": ("🖼", "Imagen"), "AUDIO": ("🔊", "Audio (se intercala en edición, no pares)"),
    "SLIDE": ("📊", "Slide"), "OBJETIVOS": ("🎯", "Objetivos"), "ROADMAP": ("🗺", "Roadmap"),
    "PANTALLA": ("🖥", "Muestra"), "NOTA": ("✏️", "Nota"), "TAREA": ("📘", "Tarea"),
    "RECURSO": ("📎", "Recurso"), "ESCENA": ("🎥", "Cambia a escena"),
}
_RE_BLOQUE = re.compile(r"\[(TAREA|RECURSO)(?::\s*([^\]]*))?\](.*?)\[/\1\]", re.S)


def _chip(tipo: str, valor: str) -> str:
    icono, nombre = ICONOS.get(tipo, ("•", tipo))
    texto = f"{nombre}: {valor}" if valor else nombre
    return f'<span class="cue cue-{tipo.lower()}">{icono} {html.escape(texto)}</span>'


def plan_escenas(cuerpo: str, por_defecto: str, pantalla: str) -> tuple[str, list[tuple[str, str]]]:
    """Inserta avisos [ESCENA: X] y devuelve (texto, [(escena, sección), ...]).

    Regla sin etiquetas extra: se empieza en la escena por defecto (cámara); cada
    [PANTALLA] cambia a la escena de pantalla hasta el siguiente título.
    """
    salida, cambios = [f"[ESCENA: {por_defecto}]"], [(por_defecto, "inicio")]
    actual, seccion = por_defecto, "inicio"
    for linea in cuerpo.splitlines():
        es_titulo = linea.lstrip().startswith("#")
        if es_titulo:
            seccion = linea.lstrip("# ").strip()
        if "[PANTALLA" in linea and actual != pantalla:
            salida.append(f"[ESCENA: {pantalla}]")
            actual = pantalla
            cambios.append((pantalla, seccion))
        salida.append(linea)
        if es_titulo and actual != por_defecto:
            salida.append(f"[ESCENA: {por_defecto}]")
            actual = por_defecto
            cambios.append((por_defecto, seccion))
    return "\n".join(salida), cambios


def cuerpo_teleprompter(g: Guion, por_defecto: str = "Camara", pantalla: str = "Clase") -> str:
    """Markdown del guion -> HTML con las etiquetas convertidas en avisos visuales."""
    texto = _RE_BLOQUE.sub(lambda m: _chip(m[1], (m[2] or "").strip() + " (en el workbook)"), g.cuerpo)
    texto, _ = plan_escenas(texto, por_defecto, pantalla)
    texto = PATRON_ETIQUETA.sub(lambda m: "" if m["cierre"] else _chip(m["tipo"], (m["valor"] or "").strip()), texto)
    return markdown.markdown(texto)


def _escenas(cfg: Config) -> tuple[str, str]:
    obs = cfg.get("obs", {}) or {}
    return obs.get("escena_por_defecto", "Camara"), obs.get("escena_pantalla", "Clase")


def teleprompter(g: Guion, lec: Leccion, cfg: Config) -> Path:
    plantilla = (cfg.ruta("plantillas") / "teleprompter.html").read_text(encoding="utf-8")
    pagina = (plantilla
              .replace("{{TITULO}}", html.escape(f"{lec.id} · {lec.titulo}"))
              .replace("{{DURACION}}", f"{g.minutos_estimados:.1f}")
              .replace("{{CUERPO}}", cuerpo_teleprompter(g, *_escenas(cfg))))
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
        "- [ ] OBS: colección de escenas *SWA* (ver docs/GUIA_GRABACION_OBS.md), 1920x1080, 30 fps, MKV con remux a MP4",
        "- [ ] OBS: micrófono en la pista de audio 1, picos entre -12 y -6 dB",
        "- [ ] Notificaciones del sistema desactivadas; pestañas no necesarias cerradas",
        "- [ ] Agua, luz frontal y cámara a la altura de los ojos",
        "",
        "## Ten abierto en pantalla (en este orden)",
    ]
    pantallas = g.de_tipo("PANTALLA")
    lineas += [f"{i}. [ ] {e.valor}  _(sección: {e.seccion})_" for i, e in enumerate(pantallas, 1)] or ["- (nada: lección solo a cámara)"]

    _, cambios = plan_escenas(g.cuerpo, *_escenas(cfg))
    lineas += ["", "## Cambios de escena en OBS (también aparecen en el teleprompter)"]
    lineas += [f"{i}. **{esc}** — {sec}" for i, (esc, sec) in enumerate(cambios, 1)]

    lineas += ["", "## Visuales que se insertarán en edición (no hace falta mostrarlos al grabar)"]
    for item in plan:
        ok = "x" if item.destino.exists() else " "
        lineas.append(f"- [{ok}] {item.tipo:<9} `{item.relativo}` — {item.descripcion}")
    if any(not i.destino.exists() for i in plan):
        lineas += ["", f"> Faltan assets. Ejecuta: `python builder.py preparar {lec.modulo:02d} {lec.numero:02d} --generar`"]
    if g.de_tipo("AUDIO"):
        lineas += ["", "> Los [AUDIO] se intercalan en edición con una tarjeta «Escucha»: al grabar, sigue leyendo sin pausa."]

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

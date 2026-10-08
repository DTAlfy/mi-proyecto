"""Workbook PDF por módulo: TAREAS + RECURSOS de cada guion + capturas + CTA.

Renderizado: Markdown -> HTML autocontenido (imágenes embebidas) -> PDF con el
modo headless de Edge/Chrome, que ya está instalado en Windows y macOS.
Sin wkhtmltopdf (abandonado) ni LaTeX (pesado).
"""

from __future__ import annotations

import base64
import html
import mimetypes
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import markdown

from . import guion as guion_mod
from . import materiales as materiales_mod
from .config import Config
from .naming import Leccion, iterar_lecciones, material, pista_audio, roadmap as nombre_roadmap, workbook

NAVEGADORES = (
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
)
_RE_IMG = re.compile(r'(<img[^>]*src=")([^"]+)(")')


def _data_uri(ruta: Path) -> str:
    tipo = mimetypes.guess_type(ruta.name)[0] or "image/png"
    return f"data:{tipo};base64,{base64.b64encode(ruta.read_bytes()).decode()}"


def _embeber_imagenes(fragmento: str, base: Path) -> str:
    def sustituir(m: re.Match[str]) -> str:
        src = m.group(2)
        if src.startswith(("http", "data:")):
            return m.group(0)
        ruta = (base / src).resolve()
        return m.group(1) + (_data_uri(ruta) if ruta.exists() else src) + m.group(3)
    return _RE_IMG.sub(sustituir, fragmento)


def capturas(cfg: Config, lec: Leccion) -> list[Path]:
    """Capturas de Lightshot/Flameshot guardadas como CAPTURAS/M01_L01_loquesea.png"""
    carpeta = cfg.ruta("assets") / "CAPTURAS"
    return sorted(p for p in carpeta.glob(f"{lec.id}_*") if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"))


def construir_html(modulo: int, cfg: Config, curriculo: dict[str, Any]) -> tuple[str, list[str]]:
    """Devuelve (html, avisos)."""
    avisos: list[str] = []
    mod = next(m for m in curriculo["modulos"] if m["numero"] == modulo)
    marca, enlaces = cfg["proyecto"]["marca"], cfg["proyecto"].get("enlaces", {})
    md = lambda t: markdown.markdown(t, extensions=["tables", "sane_lists"])  # noqa: E731

    secciones: list[str] = []
    for lec in (l for l in iterar_lecciones(curriculo) if l.modulo == modulo):
        ruta = cfg.ruta("guiones") / lec.guion
        if not ruta.exists():
            avisos.append(f"{lec.guion} no existe todavía (se omite)")
            continue
        g = guion_mod.cargar(ruta)
        partes = [f'<section class="leccion"><p class="id">{lec.id}</p><h2>{html.escape(lec.titulo)}</h2>',
                  f'<p class="objetivo">{html.escape(lec.objetivo)}</p>']
        for b in g.bloques:
            clase = b.tipo.lower()
            partes.append(f'<div class="bloque {clase}"><h3>{"✍️ Tarea" if b.tipo == "TAREA" else "📎 Recurso"}: '
                          f'{html.escape(b.titulo)}</h3>{_embeber_imagenes(md(b.contenido), ruta.parent)}</div>')
        for cap in capturas(cfg, lec):
            partes.append(f'<figure><img src="{_data_uri(cap)}"><figcaption>{html.escape(cap.stem)}</figcaption></figure>')
        if not g.bloques:
            avisos.append(f"{lec.guion} no tiene bloques [TAREA] ni [RECURSO]")
        partes.append("</section>")
        secciones.append("\n".join(partes))

    # Materiales entregables del módulo (materiales.yaml)
    datos = materiales_mod.cargar()
    piezas = []
    for mat in materiales_mod.de_modulo(datos, modulo):
        if mat.get("tipo") == "audio":
            carpeta = materiales_mod.carpeta_audio(cfg, mat)
            filas = "".join(
                f"<tr><td>{pista_audio(mat['id'], i)}</td><td>{html.escape(ln['texto'])}</td>"
                f"<td>{html.escape(ln.get('traduccion', ''))}</td></tr>"
                for i, ln in enumerate(mat["lineas"], 1))
            piezas.append(f'<div class="bloque recurso"><h3>🎧 {html.escape(mat["titulo"])}</h3>'
                          f'<p>Audios en <code>{carpeta.name}/</code></p>'
                          f'<table><tr><th>Pista</th><th>Inglés</th><th>Español</th></tr>{filas}</table></div>')
        else:
            img = materiales_mod.ruta_imagen(cfg, mat)
            if img.exists():
                piezas.append(f'<figure class="material"><img src="{_data_uri(img)}">'
                              f'<figcaption>{mat["id"]} · {html.escape(mat["titulo"])}</figcaption></figure>')
            else:
                avisos.append(f"{img.name} no existe: ejecuta `builder.py materiales`")
            if mat.get("verificado") is False:
                avisos.append(f"{mat['id']} tiene cifras sin verificar (sale con sello BORRADOR)")
    from . import web as web_mod
    interactivos = web_mod.de_modulo(web_mod.cargar(), modulo)
    if interactivos:
        filas = "".join(
            f"<tr><td><b>{html.escape(re.sub(r'[*]', '', p['titulo']))}</b><br>{html.escape(p.get('lead', ''))}</td>"
            f"<td><code>{material(p['id'], p['clave'], '.html')}</code></td></tr>" for p in interactivos)
        piezas.append('<div class="bloque recurso"><h3>🖥 Materiales interactivos</h3>'
                      '<p>Ábrelos en tu navegador desde la carpeta <code>Web/</code> (empieza por <code>index.html</code>). '
                      'Funcionan sin conexión y guardan tu progreso.</p>'
                      f'<table><tr><th>Material</th><th>Archivo</th></tr>{filas}</table></div>')
    if piezas:
        secciones.append('<section class="leccion"><p class="id">MATERIALES</p><h2>Materiales para tus clases</h2>'
                         '<p class="objetivo">Descárgalos y úsalos con tus alumnos.</p>' + "\n".join(piezas) + "</section>")

    roadmap = cfg.ruta("assets") / "ROADMAP" / nombre_roadmap(modulo)
    portada_img = f'<img class="roadmap" src="{_data_uri(roadmap)}">' if roadmap.exists() else ""
    plantilla = (cfg.ruta("plantillas") / "workbook.html").read_text(encoding="utf-8")
    reemplazos = {
        "{{CURSO}}": html.escape(curriculo["curso"]["titulo"]),
        "{{MODULO}}": f"Módulo {modulo}: {html.escape(mod['titulo'])}",
        "{{HITO}}": html.escape(mod.get("hito", "")),
        "{{ROADMAP}}": portada_img,
        "{{SECCIONES}}": "\n".join(secciones),
        "{{TIDYCAL}}": enlaces.get("tidycal", "#"),
        "{{SKOOL}}": enlaces.get("skool", "#"),
        "{{AUTOR}}": html.escape(cfg["proyecto"].get("autor", "")),
        "{{PRIMARIO}}": marca["color_primario"],
        "{{SECUNDARIO}}": marca["color_secundario"],
    }
    for k, v in reemplazos.items():
        plantilla = plantilla.replace(k, v)
    return plantilla, avisos


def buscar_navegador() -> str | None:
    if (propio := os.environ.get("SWA_NAVEGADOR")) and Path(propio).exists():
        return propio
    for nombre in ("msedge", "chrome", "google-chrome", "chromium", "chromium-browser"):
        if (ruta := shutil.which(nombre)):
            return ruta
    return next((n for n in NAVEGADORES if Path(n).exists()), None)


def a_pdf(html_path: Path, pdf_path: Path, navegador: str) -> None:
    args = [navegador, "--headless", "--disable-gpu", "--no-pdf-header-footer", "--print-to-pdf-no-header",
            f"--print-to-pdf={pdf_path}", html_path.resolve().as_uri()]
    if sys.platform.startswith("linux"):
        args.insert(1, "--no-sandbox")
    subprocess.run(args, check=True, capture_output=True, timeout=180)


def generar(modulo: int, cfg: Config, curriculo: dict[str, Any], solo_html: bool = False) -> tuple[Path, list[str]]:
    contenido, avisos = construir_html(modulo, cfg, curriculo)
    carpeta = cfg.ruta("workbooks")
    html_path = carpeta / workbook(modulo, ".html")
    html_path.write_text(contenido, encoding="utf-8")
    if solo_html:
        return html_path, avisos
    navegador = buscar_navegador()
    if not navegador:
        avisos.append("No encontré Edge/Chrome: abre el .html y usa Imprimir > Guardar como PDF.")
        return html_path, avisos
    pdf_path = carpeta / workbook(modulo, ".pdf")
    a_pdf(html_path, pdf_path, navegador)
    return pdf_path, avisos

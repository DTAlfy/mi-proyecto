"""Visuales generados en local (coste $0): slides de texto y Roadmap de Ingresos.

Por qué en local y no con IA: los modelos de imagen todavía escriben mal el
texto (letras deformadas, tildes perdidas). Para slides y el roadmap, que son
casi solo texto, Pillow da un resultado nítido, coherente con la marca y gratis.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

_FUENTES_SISTEMA = (
    "arialbd.ttf", "arial.ttf",                                   # Windows
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",          # macOS
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",       # Linux
    "DejaVuSans-Bold.ttf",
)


def _hex(color: str) -> tuple[int, int, int]:
    color = color.lstrip("#")
    return tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def _fuente(marca: dict[str, Any], tam: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidatas = [marca.get("fuente_ttf")] if marca.get("fuente_ttf") else []
    for nombre in [*candidatas, *_FUENTES_SISTEMA]:
        try:
            return ImageFont.truetype(nombre, tam)
        except OSError:
            continue
    return ImageFont.load_default(size=tam)


def _envolver(draw: ImageDraw.ImageDraw, texto: str, fuente: Any, ancho_max: int) -> list[str]:
    lineas, actual = [], ""
    for palabra in texto.split():
        prueba = f"{actual} {palabra}".strip()
        if draw.textlength(prueba, font=fuente) <= ancho_max:
            actual = prueba
        else:
            if actual:
                lineas.append(actual)
            actual = palabra
    if actual:
        lineas.append(actual)
    return lineas


def slide(titulo: str, puntos: list[str], destino: Path, marca: dict[str, Any],
          tam: tuple[int, int] = (1920, 1080), pie: str = "") -> Path:
    """Slide 16:9: título grande + hasta 4 viñetas. Fondo de marca, sin plantillas externas."""
    w, h = tam
    img = Image.new("RGB", tam, _hex(marca["color_fondo"]))
    d = ImageDraw.Draw(img)
    margen = int(w * 0.08)
    d.rectangle([0, 0, int(w * 0.012), h], fill=_hex(marca["color_primario"]))

    f_titulo, f_punto, f_pie = _fuente(marca, int(h * 0.075)), _fuente(marca, int(h * 0.048)), _fuente(marca, int(h * 0.025))
    y = int(h * 0.14)
    for ln in _envolver(d, titulo, f_titulo, w - 2 * margen):
        d.text((margen, y), ln, font=f_titulo, fill=_hex(marca["color_secundario"]))
        y += int(h * 0.095)
    y += int(h * 0.04)
    for punto in puntos[:4]:
        cy = y + int(h * 0.028)
        r = int(h * 0.011)
        d.ellipse([margen, cy - r, margen + 2 * r, cy + r], fill=_hex(marca["color_primario"]))
        for i, ln in enumerate(_envolver(d, punto, f_punto, w - 2 * margen - 4 * r)):
            d.text((margen + 4 * r, y), ln, font=f_punto, fill=_hex(marca["color_texto"]))
            y += int(h * 0.065)
        y += int(h * 0.025)
    if pie:
        d.text((margen, h - int(h * 0.07)), pie, font=f_pie, fill=_hex(marca["color_suave"]))
    destino.parent.mkdir(parents=True, exist_ok=True)
    img.save(destino)
    return destino


def roadmap(curriculo: dict[str, Any], modulo_actual: int, destino: Path, marca: dict[str, Any],
            tam: tuple[int, int] = (1920, 1080)) -> Path:
    """Roadmap de Ingresos: un hito por módulo; completados ✓, actual resaltado, futuros en gris.

    Sustituye las capturas manuales de Excalidraw/Miro: se regenera solo cuando
    cambia el currículo y siempre es coherente con él.
    """
    w, h = tam
    modulos = curriculo["modulos"]
    img = Image.new("RGB", tam, _hex(marca["color_fondo"]))
    d = ImageDraw.Draw(img)
    prim, sec, suave, texto = (_hex(marca[k]) for k in ("color_primario", "color_secundario", "color_suave", "color_texto"))

    f_titulo, f_mod, f_hito = _fuente(marca, int(h * 0.06)), _fuente(marca, int(h * 0.03)), _fuente(marca, int(h * 0.026))
    d.text((int(w * 0.06), int(h * 0.08)), "Roadmap de Ingresos", font=f_titulo, fill=sec)
    sub = curriculo.get("curso", {}).get("titulo", "")
    d.text((int(w * 0.06), int(h * 0.17)), sub, font=f_mod, fill=suave)

    n = len(modulos)
    x0, x1, y = int(w * 0.09), int(w * 0.91), int(h * 0.52)
    paso = (x1 - x0) / max(n - 1, 1)
    r = int(h * 0.045)
    idx_actual = next((i for i, m in enumerate(modulos) if m["numero"] == modulo_actual), 0)

    d.line([x0, y, x1, y], fill=suave, width=int(h * 0.012))
    d.line([x0, y, x0 + paso * idx_actual, y], fill=prim, width=int(h * 0.012))

    for i, mod in enumerate(modulos):
        cx = x0 + paso * i
        if i < idx_actual:
            d.ellipse([cx - r, y - r, cx + r, y + r], fill=prim)
            d.line([cx - r * 0.45, y, cx - r * 0.1, y + r * 0.4, cx + r * 0.5, y - r * 0.4], fill=(255, 255, 255), width=int(r * 0.22))
        elif i == idx_actual:
            d.ellipse([cx - r * 1.35, y - r * 1.35, cx + r * 1.35, y + r * 1.35], outline=prim, width=int(r * 0.18))
            d.ellipse([cx - r, y - r, cx + r, y + r], fill=prim)
        else:
            d.ellipse([cx - r, y - r, cx + r, y + r], fill=_hex(marca["color_fondo"]), outline=suave, width=int(r * 0.15))

        etiqueta = f"M{mod['numero']:02d}"
        color = texto if i <= idx_actual else suave
        tw = d.textlength(etiqueta, font=f_mod)
        d.text((cx - tw / 2, y - r * 2.6), etiqueta, font=f_mod, fill=color)
        for j, ln in enumerate(_envolver(d, mod.get("hito", mod["titulo"]), f_hito, int(paso * 0.95))):
            lw = d.textlength(ln, font=f_hito)
            d.text((cx - lw / 2, y + r * 1.9 + j * h * 0.038), ln, font=f_hito, fill=color)

    actual = modulos[idx_actual]
    pie = f"Estás aquí → Módulo {actual['numero']}: {actual['titulo']}"
    d.text((int(w * 0.06), int(h * 0.84)), pie, font=f_mod, fill=prim)
    destino.parent.mkdir(parents=True, exist_ok=True)
    img.save(destino)
    return destino

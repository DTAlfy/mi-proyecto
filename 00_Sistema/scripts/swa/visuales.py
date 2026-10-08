"""Composición de visuales en local (Pillow): texto exacto + ilustraciones de Apimart.

Modelo HÍBRIDO: Apimart genera la ilustración (sin texto) y aquí se compone el
texto exacto encima. Los modelos de imagen aún deforman letras, tildes y cifras;
en un mapa MCER o una plantilla un "DELE B1" mal escrito no es aceptable.
Si la ilustración aún no existe, el layout ocupa todo el ancho (sirve de vista previa gratis).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont, ImageOps

from .naming import modulos_roadmap

Tam = tuple[int, int]
_FUENTES_SISTEMA = (
    "arialbd.ttf", "arial.ttf",                                   # Windows
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",          # macOS
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",       # Linux
    "DejaVuSans-Bold.ttf",
)


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def _hex(color: str) -> tuple[int, int, int]:
    color = color.lstrip("#")
    return tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def _mezcla(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(int(x + (y - x) * t) for x, y in zip(a, b))  # type: ignore[return-value]


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
    for palabra in str(texto).split():
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


def _texto(d: ImageDraw.ImageDraw, xy: tuple[float, float], texto: str, fuente: Any, color: Any,
           ancho_max: int, interlineado: float = 1.25, centrado: bool = False) -> float:
    """Escribe texto envuelto y devuelve la y final."""
    x, y = xy
    alto = fuente.size if hasattr(fuente, "size") else 20
    for ln in _envolver(d, texto, fuente, ancho_max):
        dx = (ancho_max - d.textlength(ln, font=fuente)) / 2 if centrado else 0
        d.text((x + dx, y), ln, font=fuente, fill=color)
        y += alto * interlineado
    return y


def _lienzo(marca: dict[str, Any], tam: Tam) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", tam, _hex(marca["color_fondo"]))
    return img, ImageDraw.Draw(img)


def _guardar(img: Image.Image, destino: Path) -> Path:
    destino.parent.mkdir(parents=True, exist_ok=True)
    img.save(destino)
    return destino


def _panel_ilustracion(img: Image.Image, ruta: Path | None, caja: tuple[int, int, int, int], radio: int = 36) -> bool:
    """Pega la ilustración recortada a la caja con esquinas redondeadas. False si no hay ilustración."""
    if ruta is None or not Path(ruta).exists():
        return False
    x0, y0, x1, y1 = caja
    ilus = ImageOps.fit(Image.open(ruta).convert("RGB"), (x1 - x0, y1 - y0), Image.LANCZOS)
    mascara = Image.new("L", ilus.size, 0)
    ImageDraw.Draw(mascara).rounded_rectangle([0, 0, *ilus.size], radio, fill=255)
    img.paste(ilus, (x0, y0), mascara)
    return True


def _cabecera(d: ImageDraw.ImageDraw, marca: dict[str, Any], tam: Tam, titulo: str, subtitulo: str,
              ancho: int) -> int:
    w, h = tam
    m = int(w * 0.06)
    d.rectangle([0, 0, int(w * 0.012), h], fill=_hex(marca["color_primario"]))
    y = _texto(d, (m, int(h * 0.07)), titulo, _fuente(marca, int(h * 0.062)), _hex(marca["color_secundario"]), ancho, 1.15)
    if subtitulo:
        y = _texto(d, (m, y + h * 0.01), subtitulo, _fuente(marca, int(h * 0.028)), _hex(marca["color_suave"]), ancho)
    return int(y + h * 0.04)


def _pie(d: ImageDraw.ImageDraw, marca: dict[str, Any], tam: Tam, texto: str) -> None:
    if texto:
        w, h = tam
        d.text((int(w * 0.06), h - int(h * 0.06)), texto, font=_fuente(marca, int(h * 0.022)), fill=_hex(marca["color_suave"]))


def _borrador(img: Image.Image, marca: dict[str, Any], texto: str = "BORRADOR · VERIFICAR CIFRAS") -> None:
    w, h = img.size
    capa = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dc = ImageDraw.Draw(capa)
    f = _fuente(marca, int(h * 0.03))
    tw = dc.textlength(texto, font=f)
    y = h - h * 0.075  # esquina inferior derecha: no tapa título ni ilustración
    dc.rounded_rectangle([w - tw - 90, y, w - 30, y + h * 0.055], 12, fill=(*_hex(marca["color_primario"]), 230))
    dc.text((w - tw - 60, y + h * 0.011), texto, font=f, fill=(255, 255, 255, 255))
    img.paste(Image.alpha_composite(img.convert("RGBA"), capa).convert("RGB"))


# ---------------------------------------------------------------------------
# Visuales de lección
# ---------------------------------------------------------------------------

def slide(titulo: str, puntos: list[str], destino: Path, marca: dict[str, Any],
          tam: Tam = (1920, 1080), pie: str = "") -> Path:
    """Slide 16:9: título grande + hasta 5 viñetas."""
    w, h = tam
    img, d = _lienzo(marca, tam)
    m = int(w * 0.08)
    d.rectangle([0, 0, int(w * 0.012), h], fill=_hex(marca["color_primario"]))
    y = _texto(d, (m, int(h * 0.14)), titulo, _fuente(marca, int(h * 0.075)), _hex(marca["color_secundario"]), w - 2 * m, 1.25)
    y += int(h * 0.04)
    f_punto, r = _fuente(marca, int(h * 0.048)), int(h * 0.011)
    for punto in puntos[:5]:
        cy = y + int(h * 0.028)
        d.ellipse([m, cy - r, m + 2 * r, cy + r], fill=_hex(marca["color_primario"]))
        y = _texto(d, (m + 4 * r, y), punto, f_punto, _hex(marca["color_texto"]), w - 2 * m - 4 * r, 1.35) + int(h * 0.025)
    _pie(d, marca, tam, pie)
    return _guardar(img, destino)


def objetivos(metas: list[str], destino: Path, marca: dict[str, Any], tam: Tam = (1920, 1080),
              ilustracion: Path | None = None, pie: str = "", titulo: str = "En esta clase vas a:") -> Path:
    """Tarjeta 'Goals for the class': metas numeradas + ilustración del módulo (Apimart)."""
    w, h = tam
    img, d = _lienzo(marca, tam)
    con_ilus = _panel_ilustracion(img, ilustracion, (int(w * 0.6), int(h * 0.12), int(w * 0.95), int(h * 0.88)))
    ancho = int(w * (0.48 if con_ilus else 0.84))
    m = int(w * 0.08)
    d.rectangle([0, 0, int(w * 0.012), h], fill=_hex(marca["color_primario"]))
    y = _texto(d, (m, int(h * 0.16)), titulo, _fuente(marca, int(h * 0.07)), _hex(marca["color_secundario"]), ancho, 1.2)
    y += int(h * 0.05)
    f_num, f_meta, r = _fuente(marca, int(h * 0.04)), _fuente(marca, int(h * 0.045)), int(h * 0.036)
    for i, meta in enumerate(metas[:4], 1):
        d.ellipse([m, y, m + 2 * r, y + 2 * r], fill=_hex(marca["color_primario"]))
        num = str(i)
        d.text((m + r - d.textlength(num, font=f_num) / 2, y + r * 0.42), num, font=f_num, fill=(255, 255, 255))
        y = max(_texto(d, (m + 2.8 * r, y + r * 0.3), meta, f_meta, _hex(marca["color_texto"]), int(ancho - 2.8 * r), 1.3),
                y + 2 * r) + int(h * 0.045)
    _pie(d, marca, tam, pie)
    return _guardar(img, destino)


def escucha(destino: Path, marca: dict[str, Any], tam: Tam = (1920, 1080), subtitulo: str = "") -> Path:
    """Tarjeta en pantalla mientras suena un [AUDIO] intercalado."""
    w, h = tam
    img, d = _lienzo(marca, tam)
    prim = _hex(marca["color_primario"])
    cx, cy = w // 2, int(h * 0.42)
    barras = [0.25, 0.5, 0.8, 1.0, 0.7, 0.45, 0.9, 0.6, 0.3]
    ancho_b, sep = int(w * 0.018), int(w * 0.012)
    total = len(barras) * ancho_b + (len(barras) - 1) * sep
    for i, alto in enumerate(barras):
        x = cx - total // 2 + i * (ancho_b + sep)
        ah = int(h * 0.22 * alto)
        d.rounded_rectangle([x, cy - ah // 2, x + ancho_b, cy + ah // 2], ancho_b // 2, fill=prim)
    _texto(d, (0, int(h * 0.6)), "Escucha", _fuente(marca, int(h * 0.09)), _hex(marca["color_secundario"]), w, centrado=True)
    if subtitulo:
        _texto(d, (0, int(h * 0.72)), subtitulo, _fuente(marca, int(h * 0.035)), _hex(marca["color_suave"]), w, centrado=True)
    return _guardar(img, destino)


def roadmap(curriculo: dict[str, Any], modulo_actual: int | None, destino: Path, marca: dict[str, Any],
            tam: Tam = (1920, 1080), fondo: Path | None = None) -> Path:
    """Roadmap de Ingresos: completados ✓, actual resaltado, futuros en gris.

    `modulo_actual` None (o un módulo express) = póster general sin resaltar.
    `fondo` = ilustración de Apimart difuminada detrás (opcional).
    """
    w, h = tam
    modulos = modulos_roadmap(curriculo)
    img, d = _lienzo(marca, tam)
    if fondo is not None and Path(fondo).exists():
        capa = ImageOps.fit(Image.open(fondo).convert("RGB"), tam, Image.LANCZOS)
        img = Image.blend(img, capa, 0.14)
        d = ImageDraw.Draw(img)
    prim, sec, suave, texto = (_hex(marca[k]) for k in ("color_primario", "color_secundario", "color_suave", "color_texto"))
    f_titulo, f_mod, f_hito = _fuente(marca, int(h * 0.06)), _fuente(marca, int(h * 0.03)), _fuente(marca, int(h * 0.026))
    d.text((int(w * 0.06), int(h * 0.08)), "Roadmap de Ingresos", font=f_titulo, fill=sec)
    d.text((int(w * 0.06), int(h * 0.17)), curriculo.get("curso", {}).get("titulo", ""), font=f_mod, fill=suave)

    n = len(modulos)
    x0, x1, y = int(w * 0.09), int(w * 0.91), int(h * 0.52)
    paso = (x1 - x0) / max(n - 1, 1)
    r = int(h * 0.045)
    idx = next((i for i, m in enumerate(modulos) if m["numero"] == modulo_actual), None)

    d.line([x0, y, x1, y], fill=suave if idx is not None else prim, width=int(h * 0.012))
    if idx:
        d.line([x0, y, x0 + paso * idx, y], fill=prim, width=int(h * 0.012))
    for i, mod in enumerate(modulos):
        cx = x0 + paso * i
        if idx is None:
            d.ellipse([cx - r, y - r, cx + r, y + r], fill=_hex(marca["color_fondo"]), outline=prim, width=int(r * 0.2))
        elif i < idx:
            d.ellipse([cx - r, y - r, cx + r, y + r], fill=prim)
            d.line([cx - r * 0.45, y, cx - r * 0.1, y + r * 0.4, cx + r * 0.5, y - r * 0.4], fill=(255, 255, 255), width=int(r * 0.22))
        elif i == idx:
            d.ellipse([cx - r * 1.35, y - r * 1.35, cx + r * 1.35, y + r * 1.35], outline=prim, width=int(r * 0.18))
            d.ellipse([cx - r, y - r, cx + r, y + r], fill=prim)
        else:
            d.ellipse([cx - r, y - r, cx + r, y + r], fill=_hex(marca["color_fondo"]), outline=suave, width=int(r * 0.15))
        color = texto if idx is None or i <= idx else suave
        etiqueta = f"M{mod['numero']:02d}"
        d.text((cx - d.textlength(etiqueta, font=f_mod) / 2, y - r * 2.6), etiqueta, font=f_mod, fill=color)
        for j, ln in enumerate(_envolver(d, mod.get("hito", mod["titulo"]), f_hito, int(paso * 0.95))):
            d.text((cx - d.textlength(ln, font=f_hito) / 2, y + r * 1.9 + j * h * 0.038), ln, font=f_hito, fill=color)

    if idx is not None:
        actual = modulos[idx]
        pie = f"Estás aquí → Módulo {actual['numero']}: {actual['titulo']}"
    else:
        express = next((m for m in curriculo["modulos"] if m["numero"] == modulo_actual), None)
        pie = (f"{express['titulo']} · úsalo en cualquier etapa" if express
               else "Tu camino de $5/h a $25/h")
    d.text((int(w * 0.06), int(h * 0.84)), pie, font=f_mod, fill=prim)
    return _guardar(img, destino)


# ---------------------------------------------------------------------------
# Layouts de materiales entregables (materiales.yaml)
# ---------------------------------------------------------------------------

def lista(mat: dict[str, Any], destino: Path, marca: dict[str, Any], tam: Tam = (1920, 1080),
          ilustracion: Path | None = None) -> Path:
    """Tarjetas título + detalle en 1-2 columnas (lenguaje de aula, checklists...)."""
    w, h = tam
    img, d = _lienzo(marca, tam)
    con_ilus = _panel_ilustracion(img, ilustracion, (int(w * 0.66), int(h * 0.1), int(w * 0.96), int(h * 0.9)))
    ancho_total = int(w * (0.56 if con_ilus else 0.88))
    m = int(w * 0.06)
    y0 = _cabecera(d, marca, tam, mat["titulo"], mat.get("subtitulo", ""), ancho_total)
    items = mat["items"]
    cols = 2 if len(items) > 5 else 1
    por_col = -(-len(items) // cols)
    gap = int(w * 0.015)
    ancho_col = (ancho_total - gap * (cols - 1)) // cols
    alto_disp = h - y0 - int(h * 0.09)
    alto_card = min(int(alto_disp / por_col) - gap, int(h * 0.16))
    f_t, f_d = _fuente(marca, int(alto_card * 0.24)), _fuente(marca, int(alto_card * 0.2))
    fondo_card = _mezcla(_hex(marca["color_fondo"]), (255, 255, 255), 0.8)
    for i, it in enumerate(items):
        c, f = divmod(i, por_col)
        x, y = m + c * (ancho_col + gap), y0 + f * (alto_card + gap)
        d.rounded_rectangle([x, y, x + ancho_col, y + alto_card], 18, fill=fondo_card, outline=_hex(marca["color_suave"]))
        d.rectangle([x, y + 14, x + 8, y + alto_card - 14], fill=_hex(marca["color_primario"]))
        yy = _texto(d, (x + 30, y + alto_card * 0.14), it["titulo"], f_t, _hex(marca["color_secundario"]), ancho_col - 50, 1.15)
        if it.get("detalle"):
            _texto(d, (x + 30, yy + 4), it["detalle"], f_d, _hex(marca["color_texto"]), ancho_col - 50, 1.15)
    _pie(d, marca, tam, mat.get("nota", ""))
    if not mat.get("verificado", True):
        _borrador(img, marca)
    return _guardar(img, destino)


def escalera(mat: dict[str, Any], destino: Path, marca: dict[str, Any], tam: Tam = (1920, 1080),
             ilustracion: Path | None = None) -> Path:
    """Escalones ascendentes (MCER, idioma vehicular, escalera de precios)."""
    w, h = tam
    img, d = _lienzo(marca, tam)
    con_ilus = _panel_ilustracion(img, ilustracion, (int(w * 0.7), int(h * 0.05), int(w * 0.95), int(h * 0.36)), 28)
    m = int(w * 0.06)
    y_cab = _cabecera(d, marca, tam, mat["titulo"], mat.get("subtitulo", ""), int(w * (0.6 if con_ilus else 0.88)))
    niveles = mat["niveles"]
    n = len(niveles)
    gap = int(w * 0.01)
    ancho = (w - 2 * m - gap * (n - 1)) // n
    base_y = h - int(h * 0.1)
    techo = max(y_cab, int(h * 0.4))
    alto_min, alto_max = int((base_y - techo) * 0.55), base_y - techo
    claro, prim = _mezcla(_hex(marca["color_primario"]), (255, 255, 255), 0.55), _hex(marca["color_primario"])
    f_nivel, f_nombre, f_linea = _fuente(marca, int(h * 0.055)), _fuente(marca, int(h * 0.026)), _fuente(marca, int(h * 0.022))
    for i, nv in enumerate(niveles):
        t = i / max(n - 1, 1)
        alto = int(alto_min + (alto_max - alto_min) * t)
        x, y = m + i * (ancho + gap), base_y - alto
        d.rounded_rectangle([x, y, x + ancho, base_y], 18, fill=_mezcla(claro, prim, t))
        yy = _texto(d, (x + 18, y + 16), str(nv["nivel"]), f_nivel, (255, 255, 255), ancho - 36, 1.1)
        if nv.get("nombre"):
            yy = _texto(d, (x + 18, yy), nv["nombre"], f_nombre, (255, 255, 255), ancho - 36, 1.2) + 8
        for linea in nv.get("lineas", []):
            yy = _texto(d, (x + 18, yy), linea, f_linea, (255, 255, 255), ancho - 36, 1.2) + 4
    _pie(d, marca, tam, mat.get("nota", ""))
    if not mat.get("verificado", True):
        _borrador(img, marca)
    return _guardar(img, destino)


def linea_tiempo(mat: dict[str, Any], destino: Path, marca: dict[str, Any], tam: Tam = (1920, 1080),
                 ilustracion: Path | None = None) -> Path:
    """Barra segmentada proporcional a los minutos (estructura de clase)."""
    w, h = tam
    img, d = _lienzo(marca, tam)
    con_ilus = _panel_ilustracion(img, ilustracion, (int(w * 0.72), int(h * 0.05), int(w * 0.95), int(h * 0.34)), 28)
    m = int(w * 0.06)
    _cabecera(d, marca, tam, mat["titulo"], mat.get("subtitulo", ""), int(w * (0.62 if con_ilus else 0.88)))
    tramos = mat["tramos"]
    total = sum(t["minutos"] for t in tramos)
    x, y, alto = m, int(h * 0.52), int(h * 0.11)
    ancho_total = w - 2 * m
    prim, sec = _hex(marca["color_primario"]), _hex(marca["color_secundario"])
    f_min, f_nom, f_det = _fuente(marca, int(h * 0.032)), _fuente(marca, int(h * 0.027)), _fuente(marca, int(h * 0.021))
    for i, t in enumerate(tramos):
        ancho = int(ancho_total * t["minutos"] / total)
        color = _mezcla(prim if i % 2 == 0 else sec, (255, 255, 255), 0.12 * (i // 2))
        d.rectangle([x, y, x + ancho - 4, y + alto], fill=color)
        etiqueta = f"{t['minutos']}'"
        d.text((x + (ancho - d.textlength(etiqueta, font=f_min)) / 2, y + alto * 0.3), etiqueta, font=f_min, fill=(255, 255, 255))
        ancho_txt = max(ancho - 10, int(w * 0.12))
        if i % 2 == 0:  # etiquetas alternas abajo/arriba para que no choquen en tramos cortos
            yy = _texto(d, (x, y + alto + 18), t["nombre"], f_nom, sec, ancho_txt, 1.15)
            if t.get("detalle"):
                _texto(d, (x, yy + 2), t["detalle"], f_det, _hex(marca["color_texto"]), ancho_txt, 1.2)
        else:
            lineas = len(_envolver(d, t["nombre"], f_nom, ancho_txt)) + (len(_envolver(d, t.get("detalle", ""), f_det, ancho_txt)) if t.get("detalle") else 0)
            yy = _texto(d, (x, y - 22 - lineas * f_nom.size * 1.2), t["nombre"], f_nom, sec, ancho_txt, 1.15)
            if t.get("detalle"):
                _texto(d, (x, yy + 2), t["detalle"], f_det, _hex(marca["color_texto"]), ancho_txt, 1.2)
        x += ancho
    d.text((m, y + alto + int(h * 0.27)), f"Total: {total} minutos", font=f_nom, fill=prim)
    _pie(d, marca, tam, mat.get("nota", ""))
    return _guardar(img, destino)


def plantilla(mat: dict[str, Any], destino: Path, marca: dict[str, Any], tam: Tam = (1920, 1080),
              ilustracion: Path | None = None) -> Path:
    """Campos con líneas para rellenar (Goals for today, feedback de clase...)."""
    w, h = tam
    img, d = _lienzo(marca, tam)
    con_ilus = _panel_ilustracion(img, ilustracion, (int(w * 0.68), int(h * 0.1), int(w * 0.95), int(h * 0.9)))
    ancho = int(w * (0.56 if con_ilus else 0.88))
    m = int(w * 0.06)
    y = _cabecera(d, marca, tam, mat["titulo"], mat.get("subtitulo", ""), ancho)
    campos = mat["campos"]
    alto_campo = (h - y - int(h * 0.08)) // len(campos)
    f_campo = _fuente(marca, int(min(h * 0.032, alto_campo * 0.3)))
    for campo in campos:
        _texto(d, (m, y), campo, f_campo, _hex(marca["color_secundario"]), ancho)
        for k in (1, 2):
            yl = y + int(alto_campo * (0.35 + 0.28 * k))
            d.line([m, yl, m + ancho, yl], fill=_hex(marca["color_suave"]), width=2)
        y += alto_campo
    _pie(d, marca, tam, mat.get("nota", ""))
    return _guardar(img, destino)


LAYOUTS = {"lista": lista, "escalera": escalera, "linea_tiempo": linea_tiempo, "plantilla": plantilla}

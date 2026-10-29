"""Genera la guía PDF (ES y EN) a partir de config.json y contenido.json.

Uso:  python3 build_pdf.py
Salida: salidas/<archivo definido en contenido.json>
"""
import json
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Flowable, KeepTogether, PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

BASE = Path(__file__).parent
SALIDAS = BASE / "salidas"
FONT_DIR = Path("/usr/share/fonts/truetype/crosextra")

# Paleta: azul noche (confianza) + dorado (ingresos)
NAVY = HexColor("#14213D")
GOLD = HexColor("#FCA311")
INK = HexColor("#1B1F2A")
MUTED = HexColor("#5B6475")
SOFT = HexColor("#EEF1F6")

PAGE_W, PAGE_H = letter
MARGIN = 0.8 * inch


def registrar_fuentes():
    """Carlito/Caladea tienen las mismas medidas que Calibri/Cambria; si no están, usa Helvetica."""
    try:
        pdfmetrics.registerFont(TTFont("Body", str(FONT_DIR / "Carlito-Regular.ttf")))
        pdfmetrics.registerFont(TTFont("Body-Bold", str(FONT_DIR / "Carlito-Bold.ttf")))
        pdfmetrics.registerFont(TTFont("Body-Italic", str(FONT_DIR / "Carlito-Italic.ttf")))
        pdfmetrics.registerFont(TTFont("Head", str(FONT_DIR / "Caladea-Bold.ttf")))
        pdfmetrics.registerFontFamily("Body", normal="Body", bold="Body-Bold", italic="Body-Italic")
        return "Body", "Body-Bold", "Body-Italic", "Head"
    except Exception:
        return "Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Helvetica-Bold"


BODY, BOLD, ITALIC, HEAD = registrar_fuentes()

S = {
    "h1": ParagraphStyle("h1", fontName=HEAD, fontSize=24, leading=29, textColor=NAVY, spaceAfter=14),
    "p": ParagraphStyle("p", fontName=BODY, fontSize=12, leading=17, textColor=INK, spaceAfter=10),
    "nota": ParagraphStyle("nota", fontName=ITALIC, fontSize=10.5, leading=14, textColor=MUTED, spaceBefore=6),
    "card_t": ParagraphStyle("card_t", fontName=BOLD, fontSize=13, leading=16, textColor=NAVY, spaceAfter=4),
    "card_p": ParagraphStyle("card_p", fontName=BODY, fontSize=11, leading=15, textColor=INK),
    "num": ParagraphStyle("num", fontName=HEAD, fontSize=18, leading=20, textColor=NAVY, alignment=1),
    "check": ParagraphStyle("check", fontName=BODY, fontSize=12, leading=16, textColor=INK),
}


def rellenar(texto, valores):
    for clave, valor in valores.items():
        texto = texto.replace("{" + clave + "}", valor)
    return texto


class Boton(Flowable):
    """Botón dorado con todo el rectángulo clicable."""

    def __init__(self, texto, url, ancho=3.3 * inch, alto=0.55 * inch):
        super().__init__()
        self.texto, self.url, self.width, self.height = texto, url, ancho, alto

    def draw(self):
        c = self.canv
        c.setFillColor(GOLD)
        c.roundRect(0, 0, self.width, self.height, 8, stroke=0, fill=1)
        c.setFillColor(NAVY)
        c.setFont(BOLD, 13)
        c.drawCentredString(self.width / 2, self.height / 2 - 4.5, self.texto)
        c.linkURL(self.url, (0, 0, self.width, self.height), relative=1)


class Check(Flowable):
    """Casilla con marca de verificación dibujada (no depende de glifos)."""

    def __init__(self, lado=14):
        super().__init__()
        self.width = self.height = lado

    def draw(self):
        c, s = self.canv, self.width
        c.setFillColor(GOLD)
        c.roundRect(0, 0, s, s, 3, stroke=0, fill=1)
        c.setStrokeColor(NAVY)
        c.setLineWidth(1.8)
        c.lines([(s * 0.22, s * 0.52, s * 0.42, s * 0.3), (s * 0.42, s * 0.3, s * 0.8, s * 0.74)])


def tarjetas(items):
    ancho = (PAGE_W - 2 * MARGIN - 12) / 2
    celdas = [[Paragraph(t, S["card_t"]), Paragraph(d, S["card_p"])] for t, d in items]
    filas = [celdas[i:i + 2] for i in range(0, len(celdas), 2)]
    if len(filas[-1]) == 1:
        filas[-1].append("")
    tabla = Table(filas, colWidths=[ancho, ancho], hAlign="LEFT")
    estilo = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 14), ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 12), ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
    ]
    for r, fila in enumerate(filas):
        for col, celda in enumerate(fila):
            if celda:
                estilo.append(("BACKGROUND", (col, r), (col, r), SOFT))
    # Separación visual entre tarjetas con líneas blancas gruesas
    estilo += [("LINEAFTER", (0, 0), (0, -1), 6, white), ("LINEBELOW", (0, 0), (-1, -2), 6, white)]
    tabla.setStyle(TableStyle(estilo))
    return [tabla, Spacer(1, 12)]


def pasos(items, pad=12):
    filas = [[Paragraph(str(i), S["num"]), [Paragraph(t, S["card_t"]), Paragraph(d, S["card_p"])]]
             for i, (t, d) in enumerate(items, 1)]
    tabla = Table(filas, colWidths=[0.6 * inch, PAGE_W - 2 * MARGIN - 0.6 * inch], hAlign="LEFT")
    tabla.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (0, -1), GOLD),
        ("BACKGROUND", (1, 0), (1, -1), SOFT),
        ("LINEBELOW", (0, 0), (-1, -2), 6, white),
        ("TOPPADDING", (0, 0), (-1, -1), pad), ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
        ("LEFTPADDING", (1, 0), (1, -1), 14), ("RIGHTPADDING", (1, 0), (1, -1), 14),
    ]))
    return [tabla, Spacer(1, 14)]


def checklist(items):
    filas = [[Check(), Paragraph(t, S["check"])] for t in items]
    tabla = Table(filas, colWidths=[0.35 * inch, PAGE_W - 2 * MARGIN - 0.35 * inch], hAlign="LEFT")
    tabla.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (0, -1), 0),
    ]))
    return [tabla, Spacer(1, 8)]


def botones(items, cfg):
    filas = [[Boton(texto, cfg[clave])] for texto, clave in items]
    tabla = Table(filas, hAlign="LEFT")
    tabla.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 10)]))
    return [Spacer(1, 6), tabla]


def portada(c, guia, valores):
    p = guia["portada"]
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    # Motivo: círculo dorado grande, recortado por el borde
    c.setFillColor(GOLD)
    c.circle(PAGE_W - 0.9 * inch, PAGE_H - 1.6 * inch, 2.4 * inch, stroke=0, fill=1)
    c.setFillColor(NAVY)
    c.circle(PAGE_W - 0.9 * inch, PAGE_H - 1.6 * inch, 1.6 * inch, stroke=0, fill=1)

    c.setFillColor(GOLD)
    c.setFont(BOLD, 13)
    c.drawString(MARGIN, PAGE_H * 0.52, p["kicker"])

    titulo = Paragraph(p["titulo"], ParagraphStyle("ct", fontName=HEAD, fontSize=40, leading=46, textColor=white))
    w, h = titulo.wrap(PAGE_W - 2 * MARGIN - 0.6 * inch, PAGE_H)
    titulo.drawOn(c, MARGIN, PAGE_H * 0.52 - 18 - h)

    sub = Paragraph(p["subtitulo"], ParagraphStyle("cs", fontName=BODY, fontSize=16, leading=22, textColor=HexColor("#D9DEE8")))
    w2, h2 = sub.wrap(PAGE_W - 2 * MARGIN - 1 * inch, PAGE_H)
    sub.drawOn(c, MARGIN, PAGE_H * 0.52 - 18 - h - 22 - h2)

    c.setFillColor(GOLD)
    c.setFont(BOLD, 14)
    c.drawString(MARGIN, MARGIN, rellenar(p["por"], valores))


def construir(lang, contenido, cfg):
    guia = contenido[lang]["guia"]
    valores = {
        "nombre": cfg["nombre"],
        "contacto": cfg["contacto"],
        "fecha_limite": cfg[f"fecha_limite_{lang}"],
        "precio_programa": cfg["precio_programa"],
    }
    links = {"referral_url": cfg["referral_url"],
             "tidycal_url": cfg["tidycal_url"] if lang == "es" else cfg["tidycal_url_en"]}
    R = lambda t: rellenar(t, valores)  # noqa: E731

    def pie(c, doc):
        c.saveState()
        c.setFont(BODY, 9)
        c.setFillColor(MUTED)
        c.drawString(MARGIN, 0.45 * inch, R(guia["portada"]["por"]))
        c.drawRightString(PAGE_W - MARGIN, 0.45 * inch, str(doc.page))
        c.restoreState()

    story = [PageBreak()]  # la página 1 es la portada, dibujada en onFirstPage
    for i, sec in enumerate(guia["secciones"]):
        # Agrupa dos secciones por página: (quién soy + por qué), (califica + pasos), ...
        if i in (2, 4, 6):
            story.append(PageBreak())
        bloque = [Paragraph(R(sec["titulo"]), S["h1"])]
        for p in sec.get("parrafos", []):
            bloque.append(Paragraph(R(p), S["p"]))
        if "tarjetas" in sec:
            bloque += tarjetas([(R(t), R(d)) for t, d in sec["tarjetas"]])
        if "pasos" in sec:
            bloque += pasos([(R(t), R(d)) for t, d in sec["pasos"]])
        if "checklist" in sec:
            bloque += checklist([R(t) for t in sec["checklist"]])
        if "botones" in sec:
            bloque += botones(sec["botones"], links)
        if "nota" in sec:
            bloque.append(Paragraph(R(sec["nota"]), S["nota"]))
        story.append(KeepTogether(bloque))
        story.append(Spacer(1, 26))

    cierre = guia["cierre"]
    story += [Paragraph(R(cierre["titulo"]), S["h1"]), Paragraph(R(cierre["texto"]), S["p"])]
    story += botones(guia["secciones"][3]["botones"], links)
    story += [Spacer(1, 18), Paragraph(R(cierre["transparencia"]), S["nota"])]

    SALIDAS.mkdir(exist_ok=True)
    salida = SALIDAS / guia["archivo"]
    doc = SimpleDocTemplate(str(salida), pagesize=letter, leftMargin=MARGIN, rightMargin=MARGIN,
                            topMargin=MARGIN, bottomMargin=MARGIN,
                            title=guia["titulo_doc"], author=cfg["nombre"])
    doc.build(story, onFirstPage=lambda c, d: portada(c, guia, valores), onLaterPages=pie)
    print(f"OK  {salida}")


if __name__ == "__main__":
    cfg = json.loads((BASE / "config.json").read_text(encoding="utf-8"))
    contenido = json.loads((BASE / "contenido.json").read_text(encoding="utf-8"))
    for lang in ("es", "en"):
        construir(lang, contenido, cfg)

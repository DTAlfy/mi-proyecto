"""Genera los manuales internos (conversación y modelo de captación) a partir de manuales.json.

Uso:  python3 build_manuales.py
Reutiliza estilos y componentes de build_pdf.py para que todo el kit se vea igual.
"""
import json
import re
from xml.sax.saxutils import escape

from reportlab.lib.colors import white
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import CondPageBreak, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from build_pdf import (BASE, BODY, BOLD, GOLD, HEAD, INK, MARGIN, MUTED, NAVY, PAGE_W, S, SALIDAS, SOFT,
                       checklist, pasos, portada, rellenar, tarjetas)

ANCHO = PAGE_W - 2 * MARGIN

S2 = {
    "h2": ParagraphStyle("h2", fontName=HEAD, fontSize=15, leading=19, textColor=NAVY, spaceBefore=10, spaceAfter=8, keepWithNext=1),
    "g_t": ParagraphStyle("g_t", fontName=BOLD, fontSize=12, leading=15, textColor=NAVY),
    "g_lang": ParagraphStyle("g_lang", fontName=BOLD, fontSize=10, leading=12, textColor=NAVY, alignment=1),
    "g_p": ParagraphStyle("g_p", fontName=BODY, fontSize=10.5, leading=14.5, textColor=INK),
    "th": ParagraphStyle("th", fontName=BOLD, fontSize=10.5, leading=13, textColor=white),
    "td": ParagraphStyle("td", fontName=BODY, fontSize=10.5, leading=14, textColor=INK),
}


def fmt(texto, valores):
    """Escapa XML, aplica **negritas** y saltos de línea, y rellena {placeholders}."""
    t = escape(rellenar(texto, valores))
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return t.replace("\n", "<br/>")


def guion(g, F):
    filas = [[Paragraph(F(g["titulo"]), S2["g_t"]), ""]]
    for lang in ("en", "es"):
        filas.append([Paragraph(lang.upper(), S2["g_lang"]), Paragraph(F(g[lang]), S2["g_p"])])
    tabla = Table(filas, colWidths=[0.5 * inch, ANCHO - 0.5 * inch], hAlign="LEFT")
    tabla.setStyle(TableStyle([
        ("SPAN", (0, 0), (1, 0)),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 1), (0, -1), GOLD),
        ("BACKGROUND", (1, 1), (1, -1), SOFT),
        ("LINEBELOW", (0, 1), (-1, 1), 3, white),
        ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (1, 1), (1, -1), 10), ("RIGHTPADDING", (1, 1), (1, -1), 10),
    ]))
    return KeepTogether([tabla, Spacer(1, 12)])


def tabla(t, F):
    filas = [[Paragraph(F(c), S2["th"]) for c in t["cols"]]]
    filas += [[Paragraph(F(c), S2["td"]) for c in fila] for fila in t["filas"]]
    tb = Table(filas, colWidths=[ANCHO * a for a in t["anchos"]], hAlign="LEFT", repeatRows=1)
    estilo = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]
    estilo += [("BACKGROUND", (0, r), (-1, r), SOFT) for r in range(2, len(filas), 2)]
    tb.setStyle(TableStyle(estilo))
    return [tb, Spacer(1, 12)]


def construir(doc_def, cfg):
    valores = {
        "nombre": cfg["nombre"], "contacto": cfg["contacto"], "precio_programa": cfg["precio_programa"],
        "fecha_limite_es": cfg["fecha_limite_es"], "fecha_limite_en": cfg["fecha_limite_en"],
    }
    F = lambda t: fmt(t, valores)  # noqa: E731
    cubierta = {"portada": {**{k: rellenar(v, valores) for k, v in doc_def["portada"].items()}, "por": "Por {nombre}"}}

    story = [PageBreak()]  # la página 1 es la portada
    for i, sec in enumerate(doc_def["secciones"]):
        # Las secciones fluyen; solo saltan de página si queda poco espacio
        if i:
            story += [Spacer(1, 18), CondPageBreak(3 * inch)]
        story.append(Paragraph(F(sec["titulo"]), S["h1"]))
        for b in sec["bloques"]:
            if "p" in b:
                story.append(Paragraph(F(b["p"]), S["p"]))
            elif "h2" in b:
                story.append(Paragraph(F(b["h2"]), S2["h2"]))
            elif "lista" in b:
                story += checklist([F(t) for t in b["lista"]])
            elif "pasos" in b:
                story += pasos([(F(t), F(d)) for t, d in b["pasos"]], pad=7)
            elif "tarjetas" in b:
                story += tarjetas([(F(t), F(d)) for t, d in b["tarjetas"]])
            elif "guion" in b:
                story.append(guion(b["guion"], F))
            elif "tabla" in b:
                story += tabla(b["tabla"], F)
            elif "nota" in b:
                story.append(Paragraph(F(b["nota"]), S["nota"]))

    def pie(c, d):
        c.saveState()
        c.setFont(BODY, 9)
        c.setFillColor(MUTED)
        c.drawString(MARGIN, 0.45 * inch, doc_def["titulo_doc"])
        c.drawRightString(PAGE_W - MARGIN, 0.45 * inch, str(d.page))
        c.restoreState()

    SALIDAS.mkdir(exist_ok=True)
    salida = SALIDAS / doc_def["archivo"]
    doc = SimpleDocTemplate(str(salida), pagesize=letter, leftMargin=MARGIN, rightMargin=MARGIN,
                            topMargin=MARGIN, bottomMargin=MARGIN, title=doc_def["titulo_doc"], author=cfg["nombre"])
    doc.build(story, onFirstPage=lambda c, d: portada(c, cubierta, valores), onLaterPages=pie)
    print(f"OK  {salida}")


if __name__ == "__main__":
    cfg = json.loads((BASE / "config.json").read_text(encoding="utf-8"))
    manuales = json.loads((BASE / "manuales.json").read_text(encoding="utf-8"))
    for clave in ("conversacion", "modelo"):
        construir(manuales[clave], cfg)

"""Parser de guiones .md: etiquetas, bloques, texto hablado y validación.

Formato de etiquetas (ver docs/FORMATO_GUION.md):
  En línea:  [BROLL: desc]  [IMG: desc]  [AUDIO: frase]  [SLIDE: Título | punto | punto]
             [ROADMAP]  [PANTALLA: qué mostrar]  [NOTA: indicación que no se lee]
  Bloques:   [TAREA: título] ... [/TAREA]   [RECURSO: título] ... [/RECURSO]

Cada etiqueta guarda la posición (en palabras habladas) donde aparece, que es lo
que luego permite sincronizarla con tu voz grabada.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

ETIQUETAS_LINEA = ("BROLL", "IMG", "AUDIO", "SLIDE", "ROADMAP", "PANTALLA", "NOTA")
ETIQUETAS_BLOQUE = ("TAREA", "RECURSO")
# Etiquetas que producen un archivo (y por tanto cuestan o se generan).
ETIQUETAS_ASSET = ("BROLL", "IMG", "AUDIO", "SLIDE", "ROADMAP")
PALABRAS_POR_MINUTO = 150  # ritmo de lectura natural en español

PATRON_ETIQUETA = re.compile(r"\[(?P<cierre>/)?(?P<tipo>[A-Z]+)(?::\s*(?P<valor>[^\]]*?))?\s*\]")
PATRON_COMENTARIO = re.compile(r"<!--.*?-->", re.S)
PATRON_PALABRA = re.compile(r"[\wáéíóúüñÁÉÍÓÚÜÑ$%'’-]+", re.U)


@dataclass
class Etiqueta:
    tipo: str
    valor: str
    palabra: int                 # nº de palabras habladas antes de la etiqueta
    linea: int
    contexto: list[str] = field(default_factory=list)  # últimas palabras habladas
    seccion: str = ""

    @property
    def partes(self) -> list[str]:
        """Para SLIDE: 'Título | punto 1 | punto 2' -> ['Título', 'punto 1', 'punto 2']"""
        return [p.strip() for p in self.valor.split("|") if p.strip()]


@dataclass
class Bloque:
    tipo: str     # TAREA | RECURSO
    titulo: str
    contenido: str
    seccion: str
    linea: int


@dataclass
class Guion:
    ruta: Path | None
    meta: dict[str, Any]
    cuerpo: str
    etiquetas: list[Etiqueta]
    bloques: list[Bloque]
    palabras: list[str]          # texto hablado tokenizado (para alinear con la grabación)
    errores: list[str] = field(default_factory=list)
    avisos: list[str] = field(default_factory=list)

    def de_tipo(self, *tipos: str) -> list[Etiqueta]:
        return [e for e in self.etiquetas if e.tipo in tipos]

    @property
    def minutos_estimados(self) -> float:
        return len(self.palabras) / PALABRAS_POR_MINUTO


def separar_frontmatter(texto: str) -> tuple[dict[str, Any], str, int]:
    """Devuelve (meta, cuerpo, nº de líneas que ocupaba el frontmatter)."""
    if texto.startswith("---"):
        partes = texto.split("\n---", 1)
        if len(partes) == 2:
            meta = yaml.safe_load(partes[0][3:]) or {}
            resto = partes[1].split("\n", 1)
            cuerpo = resto[1] if len(resto) > 1 else ""
            return meta, cuerpo, texto[: len(texto) - len(cuerpo)].count("\n")
    return {}, texto, 0


def palabras_habladas(fragmento: str) -> list[str]:
    """Palabras que realmente se leen: sin títulos markdown, comentarios ni énfasis."""
    fragmento = PATRON_COMENTARIO.sub(" ", fragmento)
    lineas = [ln for ln in fragmento.splitlines() if not ln.lstrip().startswith("#")]
    return PATRON_PALABRA.findall(" ".join(lineas).replace("*", " ").replace("_", " "))


def parsear(texto: str, ruta: Path | None = None) -> Guion:
    meta, cuerpo, offset = separar_frontmatter(texto)
    etiquetas: list[Etiqueta] = []
    bloques: list[Bloque] = []
    palabras: list[str] = []
    errores: list[str] = []
    seccion = ""
    bloque_abierto: dict[str, Any] | None = None
    cursor = 0

    def procesar_texto(fragmento: str) -> None:
        nonlocal seccion
        for ln in fragmento.splitlines():
            if ln.lstrip().startswith("#"):
                seccion = ln.lstrip("# ").strip()
        palabras.extend(palabras_habladas(fragmento))

    cuerpo_sin_coment = PATRON_COMENTARIO.sub(lambda m: " " * len(m.group()), cuerpo)
    for m in PATRON_ETIQUETA.finditer(cuerpo_sin_coment):
        linea = offset + cuerpo.count("\n", 0, m.start()) + 1
        previo = cuerpo[cursor : m.start()]
        tipo, valor, cierre = m["tipo"], (m["valor"] or "").strip(), bool(m["cierre"])

        if bloque_abierto is not None:
            if cierre and tipo == bloque_abierto["tipo"]:
                contenido = cuerpo[bloque_abierto["inicio"] : m.start()].strip()
                bloques.append(Bloque(tipo, bloque_abierto["titulo"], contenido,
                                      bloque_abierto["seccion"], bloque_abierto["linea"]))
                bloque_abierto = None
                cursor = m.end()
            # Cualquier otra cosa dentro de un bloque es contenido del workbook.
            continue

        procesar_texto(previo)
        cursor = m.end()

        if tipo in ETIQUETAS_BLOQUE:
            if cierre:
                errores.append(f"Línea {linea}: [/{tipo}] sin apertura")
            else:
                bloque_abierto = {"tipo": tipo, "titulo": valor or tipo.title(),
                                  "inicio": m.end(), "seccion": seccion, "linea": linea}
        elif tipo in ETIQUETAS_LINEA:
            if cierre:
                errores.append(f"Línea {linea}: [/{tipo}] no es un bloque")
            elif tipo != "ROADMAP" and not valor:
                errores.append(f"Línea {linea}: [{tipo}] necesita descripción → [{tipo}: ...]")
            else:
                etiquetas.append(Etiqueta(tipo, valor, len(palabras), linea,
                                          palabras[-8:], seccion))
        else:
            errores.append(f"Línea {linea}: etiqueta desconocida [{tipo}]")

    if bloque_abierto is not None:
        errores.append(f"Línea {bloque_abierto['linea']}: [{bloque_abierto['tipo']}] sin cierre [/{bloque_abierto['tipo']}]")
    procesar_texto(cuerpo[cursor:])

    return Guion(ruta, meta, cuerpo, etiquetas, bloques, palabras, errores)


def cargar(ruta: Path) -> Guion:
    return parsear(ruta.read_text(encoding="utf-8"), ruta)


def validar(g: Guion, leccion: Any | None = None, minutos_objetivo: float | None = None) -> Guion:
    """Rellena g.errores (bloquean el pipeline) y g.avisos (recomendaciones)."""
    if leccion is not None:
        if g.meta.get("leccion") != leccion.id:
            g.errores.append(f"Frontmatter 'leccion' debe ser {leccion.id} (es {g.meta.get('leccion')!r})")
        if g.meta.get("clave") != leccion.clave:
            g.errores.append(f"Frontmatter 'clave' debe ser {leccion.clave} (es {g.meta.get('clave')!r})")
        if g.ruta is not None and g.ruta.name != leccion.guion:
            g.errores.append(f"El archivo debe llamarse {leccion.guion}")

    if not g.de_tipo("ROADMAP"):
        g.avisos.append("Falta [ROADMAP]: el alumno debe ver dónde está en la hoja de ruta.")
    if not g.palabras:
        g.errores.append("El guion no tiene texto para leer.")
    elif len(g.palabras) >= 40 and g.etiquetas and g.etiquetas[0].palabra > 40:
        g.avisos.append("Ningún visual en el hook: añade un [BROLL] o [IMG] en los primeros 15 s.")

    for e in g.de_tipo("BROLL"):
        n = len(e.valor.split())
        if n > 8:
            g.avisos.append(f"Línea {e.linea}: [BROLL] largo ({n} palabras); prompts cortos = resultados más predecibles.")
    for e in g.de_tipo("SLIDE"):
        if len(e.partes) > 5:
            g.avisos.append(f"Línea {e.linea}: [SLIDE] con más de 4 puntos se lee mal en pantalla.")

    if minutos_objetivo and g.palabras:
        dur = g.minutos_estimados
        if dur > minutos_objetivo * 1.5:
            g.avisos.append(f"Duración estimada {dur:.1f} min (objetivo {minutos_objetivo} min): recorta.")
        elif dur < minutos_objetivo * 0.5:
            g.avisos.append(f"Duración estimada {dur:.1f} min (objetivo {minutos_objetivo} min): quizá falta desarrollo.")
    return g

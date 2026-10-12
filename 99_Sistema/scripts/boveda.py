"""Utilidades compartidas para leer la bóveda (sin dependencias externas).

Lee el frontmatter de las notas tal como lo escribe Obsidian:
    nivel: A1                     -> "A1"
    nivel: [A1, A2]               -> ["A1", "A2"]
    requiere:                     -> ["[[A1.G03 Presente regular]]", ...]
      - "[[A1.G03 Presente regular]]"
"""
import re
from pathlib import Path

NIVELES = ["A0", "A1", "A2", "B1", "B2", "C1"]

_CLAVE = re.compile(r"^([A-Za-z_][\w-]*):\s*(.*)$")
_ITEM = re.compile(r"^\s*-\s*(.*)$")
_ENLACE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")


def _limpiar(valor):
    valor = valor.strip()
    if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in "\"'":
        valor = valor[1:-1]
    return valor


def _lista_en_linea(valor):
    interior = valor.strip()[1:-1]
    partes = re.findall(r'"[^"]*"|\'[^\']*\'|[^,]+', interior)
    return [_limpiar(p) for p in partes if p.strip()]


def separar(texto):
    """Devuelve (propiedades, cuerpo)."""
    if not texto.startswith("---"):
        return {}, texto
    fin = texto.find("\n---", 3)
    if fin == -1:
        return {}, texto
    lineas = texto[3:fin].strip("\n").splitlines()
    cuerpo = texto[fin + 4:].lstrip("\n")
    props, i = {}, 0
    while i < len(lineas):
        m = _CLAVE.match(lineas[i])
        i += 1
        if not m:
            continue
        clave, valor = m.group(1), m.group(2).strip()
        if valor == "":
            items = []
            while i < len(lineas) and _ITEM.match(lineas[i]):
                items.append(_limpiar(_ITEM.match(lineas[i]).group(1)))
                i += 1
            props[clave] = items if items else ""
        elif valor.startswith("[") and valor.endswith("]") and not valor.startswith("[["):
            props[clave] = _lista_en_linea(valor)
        else:
            props[clave] = _limpiar(valor)
    return props, cuerpo


def leer(ruta):
    return separar(Path(ruta).read_text(encoding="utf-8"))


def como_lista(valor):
    if valor in (None, ""):
        return []
    return valor if isinstance(valor, list) else [valor]


def enlaces(valor):
    """Nombres de nota enlazados en una propiedad (sin ruta ni extensión)."""
    destinos = []
    for v in como_lista(valor):
        for destino in _ENLACE.findall(str(v)):
            destino = destino.strip().split("/")[-1]
            if destino.endswith(".md"):
                destino = destino[:-3]
            destinos.append(destino)
    return destinos


def indice_nivel(nivel):
    return NIVELES.index(nivel) if nivel in NIVELES else -1

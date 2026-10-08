"""Nomenclatura estricta: M[XX]_L[XX]_[PalabraClave]_[Tipo].

Todo nombre de archivo del proyecto se construye AQUÍ. Ningún otro módulo
concatena nombres a mano: así un cambio de convención se hace en un solo sitio
y la ingesta nunca se rompe por un typo.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Iterator

TIPOS_ARCHIVO = ("RAW", "FINAL", "EDICION", "TELEPROMPTER", "CHECKLIST")
EXT_RAW = (".mp4", ".mov", ".mkv")

PATRON_LECCION = re.compile(
    r"^M(?P<m>\d{2})_L(?P<l>\d{2})_(?P<clave>[A-Za-z][A-Za-z0-9]*)"
    r"(?:_(?P<tipo>" + "|".join(TIPOS_ARCHIVO) + r"))?$"
)
PATRON_ASSET = re.compile(r"^M(?P<m>\d{2})_L(?P<l>\d{2})_(?P<n>\d{3})$")
PATRON_CLAVE = re.compile(r"^[A-Z][A-Za-z0-9]*$")


@dataclass(frozen=True)
class Leccion:
    modulo: int
    numero: int
    clave: str
    titulo: str = ""
    objetivo: str = ""
    modulo_titulo: str = ""

    @property
    def id(self) -> str:
        """M01_L01"""
        return f"M{self.modulo:02d}_L{self.numero:02d}"

    @property
    def base(self) -> str:
        """M01_L01_Nicho"""
        return f"{self.id}_{self.clave}"

    def archivo(self, tipo: str | None = None, ext: str = "") -> str:
        if tipo is not None and tipo not in TIPOS_ARCHIVO:
            raise ValueError(f"Tipo desconocido: {tipo}. Usa uno de {TIPOS_ARCHIVO}")
        nombre = self.base if tipo is None else f"{self.base}_{tipo}"
        return nombre + ext

    @property
    def guion(self) -> str:
        return self.archivo(None, ".md")

    def asset(self, n: int, ext: str) -> str:
        """M01_L01_001.mp4 — numeración por tipo de asset dentro de la lección."""
        if not 1 <= n <= 999:
            raise ValueError("El número de asset debe estar entre 1 y 999")
        return f"{self.id}_{n:03d}{ext}"


def workbook(modulo: int, ext: str = ".pdf") -> str:
    return f"M{modulo:02d}_Workbook{ext}"


def analizar(nombre_sin_ext: str) -> dict[str, Any] | None:
    """Descompone un nombre válido; devuelve None si no cumple la convención."""
    m = PATRON_LECCION.match(nombre_sin_ext)
    if not m:
        return None
    return {
        "modulo": int(m["m"]),
        "leccion": int(m["l"]),
        "clave": m["clave"],
        "tipo": m["tipo"],
    }


def validar_clave(clave: str) -> None:
    if not PATRON_CLAVE.match(clave):
        raise ValueError(
            f"Clave inválida '{clave}': usa CamelCase ASCII sin tildes ni espacios (ej. 'VideoIntro')."
        )


# ---------------------------------------------------------------------------
# Currículo -> Lecciones
# ---------------------------------------------------------------------------

def iterar_lecciones(curriculo: dict[str, Any]) -> Iterator[Leccion]:
    for mod in curriculo["modulos"]:
        for lec in mod["lecciones"]:
            yield Leccion(
                modulo=int(mod["numero"]),
                numero=int(lec["numero"]),
                clave=lec["clave"],
                titulo=lec.get("titulo", ""),
                objetivo=lec.get("objetivo", ""),
                modulo_titulo=mod.get("titulo", ""),
            )


def buscar_leccion(curriculo: dict[str, Any], modulo: int, numero: int) -> Leccion:
    for lec in iterar_lecciones(curriculo):
        if lec.modulo == modulo and lec.numero == numero:
            return lec
    raise KeyError(f"M{modulo:02d}_L{numero:02d} no existe en curriculum.yaml")


def validar_curriculo(curriculo: dict[str, Any]) -> list[str]:
    """Devuelve una lista de errores (vacía = currículo válido)."""
    errores: list[str] = []
    vistos: set[str] = set()
    modulos_vistos: set[int] = set()
    for mod in curriculo.get("modulos", []):
        if mod["numero"] in modulos_vistos:
            errores.append(f"Módulo {mod['numero']} duplicado")
        modulos_vistos.add(mod["numero"])
    for lec in iterar_lecciones(curriculo):
        try:
            validar_clave(lec.clave)
        except ValueError as e:
            errores.append(f"{lec.id}: {e}")
        if lec.id in vistos:
            errores.append(f"{lec.id} duplicada")
        vistos.add(lec.id)
        if not (0 < lec.modulo < 100 and 0 < lec.numero < 100):
            errores.append(f"{lec.id}: números fuera de rango 01-99")
    return errores

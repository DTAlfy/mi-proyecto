"""Carga de configuración, rutas del proyecto y secretos (.env)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

# 00_Sistema/scripts/swa/config.py -> la raíz es 3 niveles por encima de swa/
RAIZ = Path(__file__).resolve().parents[3]
SISTEMA = RAIZ / "00_Sistema"


def cargar_env(ruta: Path | None = None) -> None:
    """Lee KEY=VALUE de .env sin pisar variables ya definidas en el sistema."""
    ruta = ruta or RAIZ / ".env"
    if not ruta.exists():
        return
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, valor = linea.split("=", 1)
        os.environ.setdefault(clave.strip(), valor.strip().strip('"').strip("'"))


def secreto(nombre: str) -> str:
    """Devuelve una API key o lanza un error claro si falta."""
    cargar_env()
    valor = os.environ.get(nombre, "").strip()
    if not valor or valor.startswith("PEGA_"):
        raise RuntimeError(
            f"Falta {nombre}. Cópialo en el archivo .env de la raíz (ver .env.example)."
        )
    return valor


@dataclass(frozen=True)
class Config:
    datos: dict[str, Any]

    def __getitem__(self, clave: str) -> Any:
        return self.datos[clave]

    def get(self, clave: str, defecto: Any = None) -> Any:
        return self.datos.get(clave, defecto)

    def ruta(self, nombre: str) -> Path:
        """Ruta absoluta de una carpeta declarada en `rutas:`; la crea si no existe."""
        p = RAIZ / self.datos["rutas"][nombre]
        p.mkdir(parents=True, exist_ok=True)
        return p


def cargar_config(ruta: Path | None = None) -> Config:
    ruta = ruta or SISTEMA / "config.yaml"
    with open(ruta, encoding="utf-8") as f:
        return Config(yaml.safe_load(f))


def cargar_curriculo(ruta: Path | None = None) -> dict[str, Any]:
    ruta = ruta or SISTEMA / "curriculum.yaml"
    with open(ruta, encoding="utf-8") as f:
        return yaml.safe_load(f)

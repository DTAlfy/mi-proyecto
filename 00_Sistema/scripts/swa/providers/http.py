"""Utilidades HTTP comunes: reintentos con backoff y extracción robusta de resultados."""

from __future__ import annotations

import logging
import time
from typing import Any, Iterator

import requests

log = logging.getLogger("swa.http")

ESTADOS_OK = {"completed", "succeeded", "success", "succeed", "done", "finished"}
ESTADOS_ERROR = {"failed", "failure", "error", "cancelled", "canceled", "rejected"}
_CLAVES_URL = ("url", "video_url", "image_url", "audio_url", "output", "result_url", "download_url")


def peticion(metodo: str, url: str, intentos: int = 4, **kwargs: Any) -> requests.Response:
    """Reintenta errores de red y 429/5xx con backoff 2s, 4s, 8s. Los 4xx restantes fallan al momento."""
    kwargs.setdefault("timeout", 120)
    for i in range(intentos):
        try:
            r = requests.request(metodo, url, **kwargs)
        except requests.RequestException as e:
            if i == intentos - 1:
                raise
            log.warning("Error de red (%s), reintento %d", e, i + 1)
        else:
            if r.status_code < 400:
                return r
            if r.status_code not in (429, 500, 502, 503, 504) or i == intentos - 1:
                raise RuntimeError(f"{metodo} {url} -> HTTP {r.status_code}: {r.text[:500]}")
            log.warning("HTTP %s, reintento %d", r.status_code, i + 1)
        time.sleep(2 ** (i + 1))
    raise RuntimeError("inalcanzable")


def _recorrer(obj: Any) -> Iterator[tuple[str, Any]]:
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k, v
            yield from _recorrer(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _recorrer(v)


def buscar_url(respuesta: Any) -> str | None:
    """Primera URL de resultado en una respuesta JSON, sin depender de su forma exacta.

    Los agregadores cambian el esquema entre modelos (data[0].url, result.videos[0],
    output...). Buscar por claves conocidas evita reescribir código por cada modelo.
    """
    for clave, valor in _recorrer(respuesta):
        if clave in _CLAVES_URL:
            if isinstance(valor, str) and valor.startswith("http"):
                return valor
            if isinstance(valor, list) and valor and isinstance(valor[0], str) and valor[0].startswith("http"):
                return valor[0]
    return None


def buscar_valor(respuesta: Any, *claves: str) -> Any:
    for clave, valor in _recorrer(respuesta):
        if clave in claves and valor not in (None, ""):
            return valor
    return None


def estado(respuesta: Any) -> str:
    valor = buscar_valor(respuesta, "status", "state", "task_status")
    return str(valor).lower() if valor is not None else ""

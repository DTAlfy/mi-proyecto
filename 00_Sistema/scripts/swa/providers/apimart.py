"""Cliente de Apimart (agregador compatible con OpenAI: imagen, video, TTS, Whisper).

Rutas, modelos y parámetros salen de config.yaml -> `apimart:`. Si Apimart cambia
un modelo o una ruta, se edita la configuración, no este archivo.
Documentación oficial: https://docs.apimart.ai
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Any

from ..config import secreto
from .http import ESTADOS_ERROR, ESTADOS_OK, buscar_url, buscar_valor, estado, peticion

log = logging.getLogger("swa.apimart")


class Apimart:
    def __init__(self, cfg: dict[str, Any]):
        self.cfg = cfg
        self.base = cfg["base_url"].rstrip("/")

    @property
    def _cabeceras(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {secreto('APIMART_API_KEY')}"}

    # -- tareas asíncronas -------------------------------------------------
    def _esperar_resultado(self, respuesta: dict[str, Any]) -> str:
        """Devuelve la URL final: inmediata si viene en la respuesta, o sondeando la tarea."""
        url = buscar_url(respuesta)
        if url:
            return url
        task_id = buscar_valor(respuesta, "task_id", "id")
        if not task_id:
            raise RuntimeError(f"Respuesta sin URL ni task_id: {str(respuesta)[:300]}")
        ruta = self.cfg["ruta_tarea"].format(task_id=task_id)
        limite = time.monotonic() + self.cfg.get("sondeo_max_s", 900)
        while time.monotonic() < limite:
            time.sleep(self.cfg.get("sondeo_intervalo_s", 8))
            datos = peticion("GET", self.base + ruta, headers=self._cabeceras).json()
            est = estado(datos)
            if est in ESTADOS_ERROR:
                raise RuntimeError(f"Tarea {task_id} falló: {str(datos)[:300]}")
            url = buscar_url(datos)
            if url and (est in ESTADOS_OK or not est):
                return url
            log.info("Tarea %s: %s", task_id, est or "en cola")
        raise TimeoutError(f"La tarea {task_id} no terminó a tiempo")

    def _descargar(self, url: str) -> bytes:
        return peticion("GET", url, timeout=300).content

    # -- API pública ---------------------------------------------------------
    def imagen(self, prompt: str, params: dict[str, Any] | None = None) -> bytes:
        extra = self.cfg.get("parametros_imagen", {}) if params is None else params
        cuerpo = {"model": self.cfg["modelo_imagen"], "prompt": prompt, **extra}
        r = peticion("POST", self.base + self.cfg["ruta_imagen"], headers=self._cabeceras, json=cuerpo).json()
        b64 = buscar_valor(r, "b64_json")
        if b64:
            import base64
            return base64.b64decode(b64)
        return self._descargar(self._esperar_resultado(r))

    def video(self, prompt: str) -> bytes:
        cuerpo = {"model": self.cfg["modelo_video"], "prompt": prompt, **self.cfg.get("parametros_video", {})}
        r = peticion("POST", self.base + self.cfg["ruta_video"], headers=self._cabeceras, json=cuerpo).json()
        return self._descargar(self._esperar_resultado(r))

    def tts(self, texto: str, voz: str | None = None) -> bytes:
        voces = self.cfg.get("voces", {})
        cuerpo = {"model": self.cfg["modelo_tts"], "input": texto,
                  "voice": voces.get(voz or "narrador", "alloy"), "response_format": "mp3"}
        return peticion("POST", self.base + self.cfg["ruta_tts"], headers=self._cabeceras, json=cuerpo).content

    def transcribir(self, audio: Path) -> dict[str, Any]:
        """Whisper con marcas de tiempo por palabra (formato OpenAI verbose_json)."""
        with open(audio, "rb") as f:
            r = peticion(
                "POST", self.base + self.cfg["ruta_transcripcion"], headers=self._cabeceras, timeout=600,
                files={"file": (audio.name, f, "audio/mpeg")},
                data={"model": self.cfg["modelo_transcripcion"], "response_format": "verbose_json",
                      "timestamp_granularities[]": "word", "language": "es"},
            )
        return r.json()

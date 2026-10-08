"""Cliente mínimo de ElevenLabs Text-to-Speech."""

from __future__ import annotations

from typing import Any

from ..config import secreto
from .http import peticion


class ElevenLabs:
    def __init__(self, cfg: dict[str, Any]):
        self.cfg = cfg

    def tts(self, texto: str) -> bytes:
        voice_id = self.cfg["voice_id"]
        if voice_id.startswith("PEGA_"):
            raise RuntimeError("Configura elevenlabs.voice_id en 00_Sistema/config.yaml")
        url = f"{self.cfg['base_url'].rstrip('/')}/v1/text-to-speech/{voice_id}"
        r = peticion(
            "POST", url,
            params={"output_format": self.cfg.get("formato", "mp3_44100_128")},
            headers={"xi-api-key": secreto("ELEVENLABS_API_KEY"), "Accept": "audio/mpeg"},
            json={
                "text": texto,
                "model_id": self.cfg["modelo"],
                "voice_settings": {
                    "stability": self.cfg.get("estabilidad", 0.5),
                    "similarity_boost": self.cfg.get("similitud", 0.75),
                },
            },
        )
        return r.content

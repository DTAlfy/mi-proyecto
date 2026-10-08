"""Cliente mínimo de ElevenLabs Text-to-Speech con voces por papel."""

from __future__ import annotations

from typing import Any

from ..config import secreto
from .http import peticion


def voice_id(cfg: dict[str, Any], voz: str | None) -> str:
    papel = voz or cfg.get("voz_por_defecto", "narrador")
    if papel not in cfg.get("voces", {}):
        raise RuntimeError(f"Voz '{papel}' no definida en config.yaml › elevenlabs.voces")
    vid = cfg["voces"][papel]
    if vid.startswith("PEGA_"):
        raise RuntimeError(f"Pega el voice ID de '{papel}' en config.yaml › elevenlabs.voces")
    return vid


class ElevenLabs:
    def __init__(self, cfg: dict[str, Any]):
        self.cfg = cfg

    def tts(self, texto: str, voz: str | None = None) -> bytes:
        url = f"{self.cfg['base_url'].rstrip('/')}/v1/text-to-speech/{voice_id(self.cfg, voz)}"
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

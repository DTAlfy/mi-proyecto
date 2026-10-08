"""Plan de edición: une Auto-Cut + guion + assets en un JSON que DaVinci ejecuta.

El script de DaVinci (00_Sistema/scripts/resolve/) solo lee este JSON y llama a
la API: no analiza audio ni parsea guiones. Así funciona en DaVinci Resolve
GRATIS (scripts lanzados desde Workspace > Scripts, solo con la librería estándar).
"""

from __future__ import annotations

import difflib
import json
import logging
import unicodedata
from pathlib import Path
from typing import Any

from . import autocut
from .assets import ItemPlan
from .config import Config
from .guion import Guion
from .naming import Leccion

log = logging.getLogger("swa.edicion")

PISTA = {"BROLL": "V2", "IMG": "V2", "SLIDE": "V2", "ROADMAP": "V2", "AUDIO": "A2"}
COLOR_MARCADOR = {"PANTALLA": "Blue", "NOTA": "Yellow", "FALTA": "Red", "TAREA": "Green", "RECURSO": "Green"}


def normalizar(palabra: str) -> str:
    sin_tildes = unicodedata.normalize("NFKD", palabra.lower())
    return "".join(c for c in sin_tildes if c.isalnum())


def alinear(palabras_guion: list[str], palabras_audio: list[dict[str, Any]]) -> dict[int, float]:
    """Índice de palabra del guion -> segundo (en el RAW) en que la dijiste.

    `palabras_audio` = [{"word": str, "start": float, "end": float}, ...] (Whisper).
    SequenceMatcher tolera improvisaciones, palabras saltadas y tomas repetidas.
    """
    a = [normalizar(p) for p in palabras_guion]
    b = [normalizar(p["word"]) for p in palabras_audio]
    mapa: dict[int, float] = {}
    for bloque in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(bloque.size):
            mapa[bloque.a + k] = float(palabras_audio[bloque.b + k]["end"])
    return mapa


def tiempo_etiqueta(palabra: int, mapa: dict[int, float]) -> float | None:
    """Momento (RAW) de la etiqueta: fin de la palabra alineada más cercana anterior."""
    anteriores = [i for i in mapa if i < palabra]
    if anteriores:
        return mapa[max(anteriores)]
    posteriores = [i for i in mapa if i >= palabra]
    return mapa[min(posteriores)] if posteriores else None


def construir(g: Guion, lec: Leccion, cfg: Config, plan_assets: list[ItemPlan], raw: Path,
              transcripcion: dict[str, Any] | None = None) -> dict[str, Any]:
    ac = cfg["autocut"]
    info = autocut.info_video(raw, ac["ffprobe"])
    duracion, fps = info["duracion"], info["fps"] or cfg["video"]["fps_por_defecto"]

    stderr = autocut.detectar_silencios(raw, ac["umbral_db"], ac["silencio_min_s"], ac["ffmpeg"])
    silencios = autocut.parsear_silencedetect(stderr, duracion)
    segmentos = autocut.segmentos_con_voz(silencios, duracion, ac["margen_s"])
    dur_final = autocut.duracion_total(segmentos)

    mapa: dict[int, float] = {}
    if transcripcion:
        palabras_audio = transcripcion.get("words") or [
            w for s in transcripcion.get("segments", []) for w in s.get("words", [])
        ]
        mapa = alinear(g.palabras, palabras_audio)
        cobertura = len(mapa) / max(len(g.palabras), 1)
        log.info("Alineación: %.0f%% de las palabras del guion encontradas en el audio", cobertura * 100)
        if cobertura < 0.3:
            log.warning("Cobertura baja: se usará estimación por palabras donde falte.")
            mapa = {}
    metodo = "transcripcion" if mapa else "estimacion"

    def momento(palabra: int) -> float:
        if mapa:
            t_raw = tiempo_etiqueta(palabra, mapa)
            if t_raw is not None:
                return round(autocut.raw_a_final(t_raw, segmentos), 3)
        return round(palabra / max(len(g.palabras), 1) * dur_final, 3)

    dur_img = cfg["davinci"]["duracion_imagen_s"]
    inserciones, marcadores = [], []
    for item in plan_assets:
        e = item.etiqueta
        t = momento(e.palabra)
        if not item.destino.exists():
            marcadores.append({"inicio_s": t, "color": COLOR_MARCADOR["FALTA"], "nombre": f"FALTA {e.tipo}",
                               "nota": f"{item.relativo} no existe. Ejecuta: builder.py assets --generar"})
            continue
        inserciones.append({
            "tipo": e.tipo, "archivo": str(item.destino.resolve()), "pista": PISTA[e.tipo],
            "inicio_s": t, "duracion_s": None if e.tipo in ("BROLL", "AUDIO") else dur_img,
            "texto": e.valor, "seccion": e.seccion,
        })
    for e in g.de_tipo("PANTALLA", "NOTA"):
        marcadores.append({"inicio_s": momento(e.palabra), "color": COLOR_MARCADOR[e.tipo],
                           "nombre": e.tipo, "nota": e.valor})

    return {
        "version": 1,
        "leccion": lec.id,
        "base": lec.base,
        "proyecto": f"{cfg['davinci']['proyecto_prefijo']}_{lec.base}",
        "raw": str(raw.resolve()),
        "fps": round(fps, 3),
        "duracion_raw_s": round(duracion, 3),
        "duracion_final_s": round(dur_final, 3),
        "segmentos": segmentos,
        "metodo_sincronizacion": metodo,
        "zoom_punch_in": cfg["davinci"]["zoom_punch_in"],
        "inserciones": sorted(inserciones, key=lambda x: x["inicio_s"]),
        "marcadores": sorted(marcadores, key=lambda x: x["inicio_s"]),
        "render": {
            "preset": cfg["davinci"]["preset_render"],
            "carpeta": str(cfg.ruta("renders").resolve()),
            "nombre": lec.archivo("FINAL"),
        },
    }


def guardar(plan: dict[str, Any], cfg: Config, lec: Leccion) -> Path:
    carpeta = cfg.ruta("ediciones")
    destino = carpeta / lec.archivo("EDICION", ".json")
    destino.write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")
    # Puntero que lee el script de DaVinci (no admite argumentos desde el menú).
    (carpeta / "ACTUAL.json").write_text(json.dumps({"plan": str(destino.resolve())}, indent=2), encoding="utf-8")
    return destino

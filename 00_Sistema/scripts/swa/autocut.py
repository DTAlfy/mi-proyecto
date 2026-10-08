"""Detección de silencios y mapa de tiempos (se ejecuta FUERA de DaVinci).

Por qué aquí y no dentro de DaVinci: la API de Resolve no tiene "cortar en el
frame X" ni "ripple delete". Lo fiable es calcular aquí los tramos con voz y que
DaVinci construya un timeline nuevo solo con esos tramos (mismo resultado que
cortar + ripple delete, sin depender de funciones que la API no ofrece).

Usa el filtro `silencedetect` de ffmpeg: sin numpy/librosa, rápido con archivos
de 1 h y exacto a nivel de muestra.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

Segmento = tuple[float, float]

_RE_INICIO = re.compile(r"silence_start:\s*(-?[\d.]+)")
_RE_FIN = re.compile(r"silence_end:\s*([\d.]+)")


def info_video(ruta: Path, ffprobe: str = "ffprobe") -> dict[str, float]:
    """Duración (s) y FPS reales del archivo."""
    salida = subprocess.run(
        [ffprobe, "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=r_frame_rate:format=duration", "-of", "json", str(ruta)],
        capture_output=True, text=True, check=True,
    ).stdout
    datos = json.loads(salida)
    num, _, den = datos["streams"][0]["r_frame_rate"].partition("/")
    return {"duracion": float(datos["format"]["duration"]), "fps": float(num) / float(den or 1)}


def parsear_silencedetect(stderr: str, duracion: float) -> list[Segmento]:
    """Convierte la salida de ffmpeg silencedetect en [(inicio, fin), ...]."""
    silencios: list[Segmento] = []
    inicio: float | None = None
    for linea in stderr.splitlines():
        if (m := _RE_INICIO.search(linea)):
            inicio = max(0.0, float(m.group(1)))
        elif (m := _RE_FIN.search(linea)) and inicio is not None:
            silencios.append((inicio, float(m.group(1))))
            inicio = None
    if inicio is not None:  # el archivo termina en silencio
        silencios.append((inicio, duracion))
    return silencios


def detectar_silencios(ruta: Path, umbral_db: float, minimo_s: float, ffmpeg: str = "ffmpeg") -> str:
    """Ejecuta ffmpeg y devuelve su stderr (donde silencedetect escribe)."""
    proc = subprocess.run(
        [ffmpeg, "-hide_banner", "-nostats", "-i", str(ruta), "-map", "0:a:0", "-af",
         f"silencedetect=noise={umbral_db}dB:d={minimo_s}", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg falló analizando {ruta.name}:\n{proc.stderr[-800:]}")
    return proc.stderr


def segmentos_con_voz(silencios: list[Segmento], duracion: float, margen: float = 0.15,
                      minimo_segmento: float = 0.3) -> list[Segmento]:
    """Invierte los silencios en tramos a conservar, dejando `margen` de aire a cada lado.

    Tramos de voz más cortos que `minimo_segmento` (clics, golpes de mesa) se descartan.
    """
    tramos: list[Segmento] = []
    cursor = 0.0
    for ini, fin in sorted(silencios):
        tramos.append((cursor, ini))
        cursor = max(cursor, fin)
    tramos.append((cursor, duracion))

    resultado: list[Segmento] = []
    for ini, fin in tramos:
        if fin - ini < minimo_segmento:
            continue
        ini, fin = max(0.0, ini - margen), min(duracion, fin + margen)
        if resultado and ini <= resultado[-1][1]:  # el margen hizo que se solapen: unir
            resultado[-1] = (resultado[-1][0], max(resultado[-1][1], fin))
        else:
            resultado.append((ini, fin))
    return [(round(a, 3), round(b, 3)) for a, b in resultado]


def duracion_total(segmentos: list[Segmento]) -> float:
    return sum(b - a for a, b in segmentos)


def raw_a_final(t: float, segmentos: list[Segmento]) -> float:
    """Tiempo en el RAW -> tiempo en el video ya cortado.

    Si `t` cae dentro de un silencio eliminado, se ajusta al inicio del siguiente tramo.
    """
    acumulado = 0.0
    for ini, fin in segmentos:
        if t < ini:
            return acumulado
        if t <= fin:
            return acumulado + (t - ini)
        acumulado += fin - ini
    return acumulado


def extraer_audio_ligero(ruta: Path, destino: Path, ffmpeg: str = "ffmpeg") -> Path:
    """Audio mono 16 kHz a 32 kbps para transcribir: ~14 MB por hora, por debajo del límite de 25 MB de Whisper."""
    subprocess.run(
        [ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-i", str(ruta), "-vn",
         "-ac", "1", "-ar", "16000", "-b:a", "32k", str(destino)],
        check=True,
    )
    return destino

"""Orquestador de assets: guion -> plan -> (dry-run | generación con caché y presupuesto).

Garantías para no tirar dinero:
  1. `--dry-run` muestra cada llamada y el coste estimado sin gastar nada.
  2. Caché por contenido (manifest.json): el mismo prompt con el mismo modelo
     nunca se paga dos veces, aunque renumeres o muevas etiquetas.
  3. Tope de presupuesto por ejecución (config: presupuesto_max_usd_por_ejecucion).
"""

from __future__ import annotations

import hashlib
import json
import logging
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from . import visuales
from .config import RAIZ, Config
from .guion import Etiqueta, Guion
from .naming import Leccion

log = logging.getLogger("swa.assets")

# tipo de etiqueta -> (subcarpeta, extensión, tipo de proveedor | None si es local)
DESTINOS: dict[str, tuple[str, str, str | None]] = {
    "BROLL": ("BROLL", ".mp4", "video"),
    "IMG": ("IMAGENES", ".png", "imagen"),
    "AUDIO": ("AUDIO", ".mp3", "tts"),
    "SLIDE": ("SLIDES", ".png", None),
    "ROADMAP": ("ROADMAP", ".png", None),
}


@dataclass
class ItemPlan:
    etiqueta: Etiqueta
    destino: Path
    clase: str | None        # "video" | "imagen" | "tts" | None (local)
    proveedor: str
    prompt: str
    huella: str
    coste: float

    @property
    def es_local(self) -> bool:
        return self.clase is None

    @property
    def relativo(self) -> str:
        return self.destino.relative_to(RAIZ).as_posix()


def _modelo(cfg: Config, proveedor: str, clase: str) -> str:
    if proveedor == "apimart":
        return cfg["apimart"].get({"video": "modelo_video", "imagen": "modelo_imagen", "tts": "modelo_tts"}[clase], "")
    if proveedor == "elevenlabs":
        return f"{cfg['elevenlabs']['modelo']}/{cfg['elevenlabs']['voice_id']}"
    return ""


def huella(*partes: Any) -> str:
    return hashlib.sha256(json.dumps(partes, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]


def planificar(g: Guion, lec: Leccion, cfg: Config) -> list[ItemPlan]:
    """Traduce las etiquetas del guion en archivos concretos con nombre definitivo."""
    base = cfg.ruta("assets")
    contadores: dict[str, int] = {}
    plan: list[ItemPlan] = []
    for e in g.etiquetas:
        if e.tipo not in DESTINOS:
            continue
        carpeta, ext, clase = DESTINOS[e.tipo]
        if e.tipo == "ROADMAP":
            destino = base / carpeta / f"M{lec.modulo:02d}_Roadmap{ext}"
        else:
            contadores[e.tipo] = contadores.get(e.tipo, 0) + 1
            destino = base / carpeta / lec.asset(contadores[e.tipo], ext)

        if clase is None:
            plan.append(ItemPlan(e, destino, None, "local", e.valor, huella(e.tipo, e.valor), 0.0))
            continue

        proveedor = cfg["proveedores"][clase]
        estilo = cfg.get("estilo_visual", {}).get({"video": "video", "imagen": "imagen"}.get(clase, ""), "")
        prompt = f"{e.valor}, {estilo}" if estilo else e.valor
        params = cfg[proveedor].get(f"parametros_{clase}", {}) if proveedor == "apimart" else {}
        plan.append(ItemPlan(e, destino, clase, proveedor, prompt,
                             huella(clase, proveedor, _modelo(cfg, proveedor, clase), prompt, params),
                             float(cfg.get("costos_usd", {}).get(clase, 0.0))))
    return plan


# ---------------------------------------------------------------------------
# Manifest (caché por contenido)
# ---------------------------------------------------------------------------

def _ruta_manifest(cfg: Config) -> Path:
    return cfg.ruta("assets") / "manifest.json"


def cargar_manifest(cfg: Config) -> dict[str, Any]:
    p = _ruta_manifest(cfg)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def guardar_manifest(cfg: Config, manifest: dict[str, Any]) -> None:
    p = _ruta_manifest(cfg)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(p)  # escritura atómica: un corte de luz no corrompe la caché


def estado_item(item: ItemPlan, manifest: dict[str, Any]) -> str:
    """'listo' | 'copiar' (ya pagado con otro nombre) | 'generar'"""
    entrada = manifest.get(item.huella)
    if entrada:
        conocidos = [entrada["archivo"], *entrada.get("copias", [])]
        if item.relativo in conocidos and item.destino.exists():
            return "listo"
        for archivo in conocidos:
            if (RAIZ / archivo).exists():
                return "copiar"
    return "generar"


# ---------------------------------------------------------------------------
# Ejecución
# ---------------------------------------------------------------------------

def _clientes(cfg: Config) -> dict[str, Any]:
    from .providers.apimart import Apimart
    from .providers.elevenlabs import ElevenLabs
    return {"apimart": Apimart(cfg["apimart"]), "elevenlabs": ElevenLabs(cfg["elevenlabs"])}


def generar(plan: list[ItemPlan], cfg: Config, curriculo: dict[str, Any], lec: Leccion,
            dry_run: bool = True, forzar_presupuesto: bool = False,
            informar: Callable[[str], None] = print) -> dict[str, int]:
    manifest = cargar_manifest(cfg)
    marca = cfg["proyecto"]["marca"]
    tam = (cfg["video"]["ancho"], cfg["video"]["alto"])
    resumen = {"listo": 0, "copiar": 0, "generar": 0, "local": 0}

    pendientes = [i for i in plan if not i.es_local and estado_item(i, manifest) == "generar"]
    coste_total = sum(i.coste for i in pendientes)
    tope = float(cfg.get("presupuesto_max_usd_por_ejecucion", 0) or 0)

    for item in plan:
        if item.es_local:
            resumen["local"] += 1
            informar(f"  [local $0] {item.relativo}")
            if not dry_run:
                if item.etiqueta.tipo == "ROADMAP":
                    visuales.roadmap(curriculo, lec.modulo, item.destino, marca, tam)
                else:
                    partes = item.etiqueta.partes
                    visuales.slide(partes[0], partes[1:], item.destino, marca, tam, pie=f"{lec.id} · {lec.titulo}")
            continue
        est = estado_item(item, manifest)
        resumen[est] += 1
        precio = f"${item.coste:.2f}" if item.coste else "$?"
        informar(f"  [{est:7}] {item.proveedor}/{item.clase} {precio:>6}  {item.relativo}  ← \"{item.etiqueta.valor}\"")

    if tope and coste_total > tope and not forzar_presupuesto:
        raise RuntimeError(
            f"Coste estimado ${coste_total:.2f} supera el tope ${tope:.2f}. "
            "Revisa el plan o usa --forzar-presupuesto."
        )
    informar(f"\n  Llamadas de pago: {len(pendientes)}  ·  Coste estimado: "
             + (f"${coste_total:.2f}" if any(i.coste for i in pendientes) else "rellena costos_usd en config.yaml"))
    if dry_run:
        informar("  (dry-run: no se ha gastado nada. Repite con --generar para ejecutar.)")
        return resumen

    clientes = _clientes(cfg) if pendientes else {}
    for item in plan:
        if item.es_local:
            continue
        est = estado_item(item, manifest)
        if est == "listo":
            continue
        item.destino.parent.mkdir(parents=True, exist_ok=True)
        if est == "copiar":
            entrada = manifest[item.huella]
            origen = next(RAIZ / a for a in [entrada["archivo"], *entrada.get("copias", [])] if (RAIZ / a).exists())
            shutil.copy2(origen, item.destino)
            entrada.setdefault("copias", [])
            if item.relativo not in entrada["copias"] and item.relativo != entrada["archivo"]:
                entrada["copias"].append(item.relativo)
            guardar_manifest(cfg, manifest)
            continue
        cliente = clientes[item.proveedor]
        log.info("Generando %s con %s", item.relativo, item.proveedor)
        datos = getattr(cliente, item.clase)(item.prompt)
        item.destino.write_bytes(datos)
        manifest[item.huella] = {
            "archivo": item.relativo, "tipo": item.etiqueta.tipo, "proveedor": item.proveedor,
            "prompt": item.prompt, "fecha": datetime.now().isoformat(timespec="seconds"),
        }
        guardar_manifest(cfg, manifest)  # tras CADA archivo: si algo falla, lo pagado no se pierde
        informar(f"  ✓ {item.relativo}")
    return resumen

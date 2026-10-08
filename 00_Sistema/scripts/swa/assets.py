"""Motor de assets: plan -> (dry-run | generación con caché y presupuesto).

Lo usan las lecciones (etiquetas del guion) y los materiales entregables
(materiales.yaml). Garantías para no tirar dinero:
  1. `--dry-run` por defecto: muestra cada llamada y el coste estimado.
  2. Caché por contenido (manifest.json): mismo prompt + modelo + voz = no se paga dos veces.
  3. Tope de presupuesto por ejecución (config: presupuesto_max_usd_por_ejecucion).
"""

from __future__ import annotations

import hashlib
import json
import logging
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from . import visuales
from .config import RAIZ, Config
from .guion import Etiqueta, Guion
from .naming import Leccion, ilustracion_modulo, roadmap

log = logging.getLogger("swa.assets")

# tipo de etiqueta -> (subcarpeta, extensión, clase de proveedor | None si es local)
DESTINOS: dict[str, tuple[str, str, str | None]] = {
    "BROLL": ("BROLL", ".mp4", "video"),
    "IMG": ("IMAGENES", ".png", "imagen"),
    "AUDIO": ("AUDIO", ".mp3", "tts"),
    "SLIDE": ("SLIDES", ".png", None),
    "OBJETIVOS": ("OBJETIVOS", ".png", None),
    "ROADMAP": ("ROADMAP", ".png", None),
}
# clase -> clave en proveedores: / costos_usd:
_PROVEEDOR_DE = {"video": "video", "imagen": "imagen", "ilustracion": "imagen", "tts": "tts"}


@dataclass
class ItemPlan:
    tipo: str                       # BROLL, IMG, AUDIO, SLIDE, OBJETIVOS, ROADMAP, ILUSTRACION, MATERIAL...
    destino: Path
    descripcion: str = ""
    clase: str | None = None        # video | imagen | ilustracion | tts | None (local, gratis)
    proveedor: str = "local"
    prompt: str = ""
    voz: str | None = None
    params: dict[str, Any] = field(default_factory=dict)
    huella: str = ""
    coste: float = 0.0
    etiqueta: Etiqueta | None = None
    render: Callable[[Path], Any] | None = None   # solo items locales

    @property
    def es_local(self) -> bool:
        return self.clase is None

    @property
    def relativo(self) -> str:
        return self.destino.relative_to(RAIZ).as_posix()


def huella(*partes: Any) -> str:
    return hashlib.sha256(json.dumps(partes, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Construcción de items
# ---------------------------------------------------------------------------

def voces_disponibles(cfg: Config) -> set[str]:
    return set(cfg[cfg["proveedores"]["tts"]].get("voces", {}))


def separar_voz(valor: str, cfg: Config) -> tuple[str | None, str]:
    """'estudiante_us | How long...?' -> ('estudiante_us', 'How long...?'); sin papel -> (None, valor)."""
    cabeza, sep, resto = valor.partition("|")
    if sep and cabeza.strip() in voces_disponibles(cfg):
        return cabeza.strip(), resto.strip()
    return None, valor.strip()


def validar_voces(g: Guion, cfg: Config) -> list[str]:
    errores = []
    for e in g.de_tipo("AUDIO"):
        voz, texto = separar_voz(e.valor, cfg)
        if voz is None and "|" in e.valor:
            papel = e.valor.split("|", 1)[0].strip()
            errores.append(f"Línea {e.linea}: voz '{papel}' no existe en config.yaml (disponibles: "
                           f"{', '.join(sorted(voces_disponibles(cfg)))})")
        if not texto:
            errores.append(f"Línea {e.linea}: [AUDIO] sin texto")
    return errores


def _modelo(cfg: Config, proveedor: str, clase: str, voz: str | None) -> str:
    if proveedor == "apimart":
        a = cfg["apimart"]
        if clase == "tts":
            return f"{a['modelo_tts']}/{a.get('voces', {}).get(voz or 'narrador', '')}"
        return a["modelo_video"] if clase == "video" else a["modelo_imagen"]
    if proveedor == "elevenlabs":
        e = cfg["elevenlabs"]
        papel = voz or e.get("voz_por_defecto", "narrador")
        return f"{e['modelo']}/{e.get('voces', {}).get(papel, '')}"
    return ""


def item_pago(clase: str, tipo: str, destino: Path, texto: str, cfg: Config, voz: str | None = None,
              etiqueta: Etiqueta | None = None, descripcion: str = "") -> ItemPlan:
    """Item que cuesta dinero: añade el estilo de marca al prompt y calcula su huella de caché."""
    proveedor = cfg["proveedores"][_PROVEEDOR_DE[clase]]
    estilo = cfg.get("estilo_visual", {}).get(clase, "") if clase != "tts" else ""
    prompt = f"{texto}, {estilo}" if estilo else texto
    params: dict[str, Any] = {}
    if proveedor == "apimart" and clase != "tts":
        params = dict(cfg["apimart"].get(f"parametros_{clase}", {}))
    return ItemPlan(
        tipo=tipo, destino=destino, descripcion=descripcion or texto, clase=clase, proveedor=proveedor,
        prompt=prompt, voz=voz, params=params, etiqueta=etiqueta,
        huella=huella(clase, proveedor, _modelo(cfg, proveedor, clase, voz), prompt, params, voz),
        coste=float(cfg.get("costos_usd", {}).get(clase, 0.0)),
    )


def item_local(tipo: str, destino: Path, render: Callable[[Path], Any], descripcion: str = "",
               etiqueta: Etiqueta | None = None) -> ItemPlan:
    return ItemPlan(tipo=tipo, destino=destino, descripcion=descripcion, render=render, etiqueta=etiqueta)


def ruta_ilustracion_modulo(cfg: Config, modulo: int) -> Path:
    return cfg.ruta("assets") / "ILUSTRACIONES" / ilustracion_modulo(modulo)


def ruta_fondo(cfg: Config, nombre: str) -> Path:
    return cfg.ruta("assets") / "ILUSTRACIONES" / f"Fondo_{nombre}.png"


def _si_existe(p: Path) -> Path | None:
    return p if p.exists() else None


def planificar(g: Guion, lec: Leccion, cfg: Config, curriculo: dict[str, Any]) -> list[ItemPlan]:
    """Traduce las etiquetas del guion en archivos con nombre definitivo."""
    base = cfg.ruta("assets")
    marca, tam = cfg["proyecto"]["marca"], (cfg["video"]["ancho"], cfg["video"]["alto"])
    pie = f"{lec.id} · {lec.titulo}"
    contadores: dict[str, int] = {}
    plan: list[ItemPlan] = []
    for e in g.etiquetas:
        if e.tipo not in DESTINOS:
            continue
        carpeta, ext, clase = DESTINOS[e.tipo]
        if e.tipo == "ROADMAP":
            destino = base / carpeta / roadmap(lec.modulo)
        else:
            contadores[e.tipo] = contadores.get(e.tipo, 0) + 1
            destino = base / carpeta / lec.asset(contadores[e.tipo], ext)

        if e.tipo == "ROADMAP":
            plan.append(item_local(e.tipo, destino, lambda d: visuales.roadmap(
                curriculo, lec.modulo, d, marca, tam, fondo=_si_existe(ruta_fondo(cfg, "roadmap"))),
                "roadmap del módulo", e))
        elif e.tipo == "SLIDE":
            partes = e.partes
            plan.append(item_local(e.tipo, destino, lambda d, p=partes: visuales.slide(
                p[0], p[1:], d, marca, tam, pie=pie), e.valor, e))
        elif e.tipo == "OBJETIVOS":
            partes = e.partes
            plan.append(item_local(e.tipo, destino, lambda d, p=partes: visuales.objetivos(
                p, d, marca, tam, ilustracion=_si_existe(ruta_ilustracion_modulo(cfg, lec.modulo)), pie=pie),
                e.valor, e))
        elif e.tipo == "AUDIO":
            voz, texto = separar_voz(e.valor, cfg)
            plan.append(item_pago("tts", e.tipo, destino, texto, cfg, voz=voz, etiqueta=e,
                                  descripcion=f"({voz}) {texto}" if voz else texto))
        else:
            plan.append(item_pago(clase, e.tipo, destino, e.valor, cfg, etiqueta=e))  # type: ignore[arg-type]
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


def _llamar(cliente: Any, item: ItemPlan) -> bytes:
    if item.clase == "video":
        return cliente.video(item.prompt)
    if item.clase == "tts":
        return cliente.tts(item.prompt, item.voz)
    return cliente.imagen(item.prompt, item.params or None)


def generar(plan: list[ItemPlan], cfg: Config, dry_run: bool = True, forzar_presupuesto: bool = False,
            informar: Callable[[str], None] = print) -> dict[str, int]:
    """Ejecuta primero los items de pago (o los simula) y después los locales.

    Los locales van al final porque pueden usar ilustraciones recién generadas.
    """
    manifest = cargar_manifest(cfg)
    resumen = {"listo": 0, "copiar": 0, "generar": 0, "local": 0}
    pagos = [i for i in plan if not i.es_local]
    pendientes = [i for i in pagos if estado_item(i, manifest) == "generar"]
    coste_total = sum(i.coste for i in pendientes)
    tope = float(cfg.get("presupuesto_max_usd_por_ejecucion", 0) or 0)

    for item in pagos:
        est = estado_item(item, manifest)
        resumen[est] += 1
        precio = f"${item.coste:.2f}" if item.coste else "$?"
        informar(f"  [{est:7}] {item.proveedor}/{item.clase} {precio:>6}  {item.relativo}  ← \"{item.descripcion}\"")

    if tope and coste_total > tope and not forzar_presupuesto:
        raise RuntimeError(f"Coste estimado ${coste_total:.2f} supera el tope ${tope:.2f}. "
                           "Revisa el plan o usa --forzar-presupuesto.")
    if pagos:
        informar(f"  Llamadas de pago: {len(pendientes)}  ·  Coste estimado: "
                 + (f"${coste_total:.2f}" if any(i.coste for i in pendientes) else "rellena costos_usd en config.yaml"))

    if not dry_run:
        clientes = _clientes(cfg) if pendientes else {}
        for item in pagos:
            est = estado_item(item, manifest)
            if est == "listo":
                continue
            item.destino.parent.mkdir(parents=True, exist_ok=True)
            if est == "copiar":
                entrada = manifest[item.huella]
                origen = next(RAIZ / a for a in [entrada["archivo"], *entrada.get("copias", [])] if (RAIZ / a).exists())
                shutil.copy2(origen, item.destino)
                if item.relativo != entrada["archivo"] and item.relativo not in entrada.setdefault("copias", []):
                    entrada["copias"].append(item.relativo)
                guardar_manifest(cfg, manifest)
                continue
            log.info("Generando %s con %s", item.relativo, item.proveedor)
            item.destino.write_bytes(_llamar(clientes[item.proveedor], item))
            manifest[item.huella] = {
                "archivo": item.relativo, "tipo": item.tipo, "proveedor": item.proveedor, "voz": item.voz,
                "prompt": item.prompt, "fecha": datetime.now().isoformat(timespec="seconds"),
            }
            guardar_manifest(cfg, manifest)  # tras CADA archivo: si algo falla, lo pagado no se pierde
            informar(f"  ✓ {item.relativo}")
    elif pagos:
        informar("  (dry-run: no se ha gastado nada. Repite con --generar para ejecutar.)")

    # Locales: gratis, se generan siempre (también en dry-run) para poder revisarlos.
    for item in plan:
        if item.es_local and item.render is not None:
            item.destino.parent.mkdir(parents=True, exist_ok=True)
            item.render(item.destino)
            resumen["local"] += 1
            informar(f"  [local $0] {item.relativo}")
    return resumen

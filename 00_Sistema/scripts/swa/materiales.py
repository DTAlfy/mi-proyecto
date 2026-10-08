"""Materiales entregables (materiales.yaml): imágenes híbridas, ilustraciones y packs de audio."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from . import visuales
from .assets import ItemPlan, item_local, item_pago, ruta_fondo, ruta_ilustracion_modulo
from .config import SISTEMA, Config
from .naming import material, pista_audio, roadmap

LAYOUTS_VALIDOS = {*visuales.LAYOUTS, "roadmap"}


def cargar(ruta: Path | None = None) -> dict[str, Any]:
    with open(ruta or SISTEMA / "materiales.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validar(datos: dict[str, Any], cfg: Config) -> list[str]:
    from .assets import voces_disponibles
    errores, vistos = [], set()
    voces = voces_disponibles(cfg)
    for mat in datos.get("materiales", []):
        id_ = mat.get("id", "?")
        if id_ in vistos:
            errores.append(f"{id_} duplicado")
        vistos.add(id_)
        try:
            material(id_, mat.get("clave", ""))
        except ValueError as e:
            errores.append(f"{id_}: {e}")
        if mat.get("tipo") == "audio":
            for i, ln in enumerate(mat.get("lineas", []), 1):
                if ln.get("voz") not in voces:
                    errores.append(f"{id_} línea {i}: voz '{ln.get('voz')}' no existe en config.yaml")
        elif mat.get("layout") not in LAYOUTS_VALIDOS:
            errores.append(f"{id_}: layout '{mat.get('layout')}' no válido ({', '.join(sorted(LAYOUTS_VALIDOS))})")
    return errores


def ruta_imagen(cfg: Config, mat: dict[str, Any]) -> Path:
    return cfg.ruta("materiales") / material(mat["id"], mat["clave"])


def carpeta_audio(cfg: Config, mat: dict[str, Any]) -> Path:
    return cfg.ruta("audios") / material(mat["id"], mat["clave"], "")


def planificar(cfg: Config, curriculo: dict[str, Any], datos: dict[str, Any],
               solo: set[str] | None = None) -> list[ItemPlan]:
    """Ilustraciones de módulo + fondos + materiales. `solo` filtra por id (MAT01, AUD02, M03, roadmap...)."""
    marca, tam = cfg["proyecto"]["marca"], (cfg["video"]["ancho"], cfg["video"]["alto"])
    ilus_dir = cfg.ruta("assets") / "ILUSTRACIONES"
    incluir = lambda clave: not solo or clave in solo  # noqa: E731
    plan: list[ItemPlan] = []

    # 1. Una ilustración por módulo: se reutiliza en [OBJETIVOS] y en la portada del workbook.
    for mod in curriculo["modulos"]:
        if mod.get("ilustracion") and incluir(f"M{mod['numero']:02d}"):
            plan.append(item_pago("ilustracion", "ILUSTRACION", ruta_ilustracion_modulo(cfg, mod["numero"]),
                                  mod["ilustracion"], cfg, descripcion=f"Módulo {mod['numero']}: {mod['ilustracion']}"))
    # 2. Fondos (16:9) para piezas generadas en local, p. ej. el roadmap.
    for nombre, prompt in (datos.get("fondos") or {}).items():
        if incluir(nombre):
            plan.append(item_pago("imagen", "FONDO", ruta_fondo(cfg, nombre), prompt, cfg, descripcion=f"Fondo {nombre}"))

    # 3. Materiales
    for mat in datos.get("materiales", []):
        if not incluir(mat["id"]):
            continue
        if mat.get("tipo") == "audio":
            for i, ln in enumerate(mat["lineas"], 1):
                plan.append(item_pago("tts", "PISTA", carpeta_audio(cfg, mat) / pista_audio(mat["id"], i),
                                      ln["texto"], cfg, voz=ln["voz"], descripcion=f"({ln['voz']}) {ln['texto']}"))
            continue
        ilus = None
        if mat.get("ilustracion"):
            ilus = ilus_dir / f"{mat['id']}.png"
            plan.append(item_pago("ilustracion", "ILUSTRACION", ilus, mat["ilustracion"], cfg,
                                  descripcion=f"{mat['id']}: {mat['ilustracion']}"))
        if mat["layout"] == "roadmap":
            render = lambda d: visuales.roadmap(curriculo, None, d, marca, tam,  # noqa: E731
                                                fondo=ruta_fondo(cfg, "roadmap"))
        else:
            fn = visuales.LAYOUTS[mat["layout"]]
            render = lambda d, m=mat, f=fn, i=ilus: f(m, d, marca, tam, ilustracion=i)  # noqa: E731
        plan.append(item_local("MATERIAL", ruta_imagen(cfg, mat), render, mat["titulo"]))

    # 4. Roadmaps por módulo (los usa [ROADMAP] y la portada del workbook).
    if not solo or "roadmap" in solo:
        for mod in curriculo["modulos"]:
            plan.append(item_local("ROADMAP", cfg.ruta("assets") / "ROADMAP" / roadmap(mod["numero"]),
                                   lambda d, n=mod["numero"]: visuales.roadmap(curriculo, n, d, marca, tam,
                                                                               fondo=ruta_fondo(cfg, "roadmap")),
                                   f"Roadmap M{mod['numero']:02d}"))
    return plan


def de_modulo(datos: dict[str, Any], modulo: int) -> list[dict[str, Any]]:
    return [m for m in datos.get("materiales", []) if m.get("modulo") == modulo]


def pendientes_de_verificar(datos: dict[str, Any]) -> list[str]:
    return [f"{m['id']} {m['clave']}" for m in datos.get("materiales", []) if m.get("verificado") is False]


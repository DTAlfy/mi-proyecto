"""Materiales web interactivos: web.yaml -> páginas HTML autocontenidas + índice.

Cada página es UN archivo (CSS y JS incrustados): se abre con doble clic, se sube a
Skool o se adjunta en un correo sin servidor ni dependencias. Las fuentes de Google
son opcionales: sin conexión se usan las del sistema.

Python solo ensambla: el diseño vive en templates/web/swa.css y los componentes
interactivos en templates/web/swa.js. Los datos que ya existen en materiales.yaml
se referencian con `fuente:` para no duplicarlos.
"""

from __future__ import annotations

import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

from . import materiales as materiales_mod
from .config import SISTEMA, Config
from .naming import material, pista_audio, workbook

COMPONENTES = ("calculadora", "diagnostico", "hitos", "titular", "cronometro", "niveles", "tarjetas")
ETIQUETA_COMPONENTE = {
    "calculadora": "Calculadora", "diagnostico": "Diagnóstico", "hitos": "Checklist", "titular": "Generador",
    "cronometro": "Cronómetro", "niveles": "Mapa interactivo", "tarjetas": "Práctica con audio",
}


def cargar(ruta: Path | None = None) -> dict[str, Any]:
    with open(ruta or SISTEMA / "web.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _materiales_por_id(mats: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {m["id"]: m for m in mats.get("materiales", [])}


def validar(web: dict[str, Any], mats: dict[str, Any]) -> list[str]:
    errores, vistos = [], set()
    por_id = _materiales_por_id(mats)
    for p in web.get("paginas", []):
        id_ = p.get("id", "?")
        if id_ in vistos:
            errores.append(f"{id_} duplicado")
        vistos.add(id_)
        try:
            material(id_, p.get("clave", ""), ".html")
        except ValueError as e:
            errores.append(f"{id_}: {e}")
        if not str(id_).startswith("WEB"):
            errores.append(f"{id_}: los materiales web usan ids WEB01..WEB99")
        if p.get("componente") not in COMPONENTES:
            errores.append(f"{id_}: componente '{p.get('componente')}' no existe ({', '.join(COMPONENTES)})")
        d = p.get("datos", {}) or {}
        fuentes = [d.get("fuente"), d.get("fuente_niveles"), d.get("fuente_idioma"), *[m.get("fuente") for m in d.get("mazos", [])]]
        for f in filter(None, fuentes):
            if f not in por_id:
                errores.append(f"{id_}: fuente '{f}' no existe en materiales.yaml")
    return errores


# ---------------------------------------------------------------------------
# Datos de cada componente
# ---------------------------------------------------------------------------

def resolver_datos(p: dict[str, Any], web: dict[str, Any], mats: dict[str, Any], cfg: Config) -> dict[str, Any]:
    """Completa los datos de la página con los comunes y con las fuentes de materiales.yaml."""
    comun = web.get("comun", {})
    d = json.loads(json.dumps(p.get("datos", {}) or {}))  # copia profunda
    por_id = _materiales_por_id(mats)
    for k in ("moneda", "meta_mensual", "semanas_por_mes"):
        d.setdefault(k, comun.get(k))

    comp = p["componente"]
    if comp == "cronometro" and d.get("fuente"):
        frases = d.get("frases", {})
        d["fases"] = [{"nombre": t["nombre"], "minutos": t["minutos"], "detalle": t.get("detalle", ""),
                       "frases": frases.get(t["nombre"], [])} for t in por_id[d["fuente"]]["tramos"]]
    elif comp == "niveles":
        fuente = por_id[d["fuente_niveles"]]
        idioma = {str(n["nivel"]): n for n in por_id[d["fuente_idioma"]]["niveles"]} if d.get("fuente_idioma") else {}
        d["niveles"] = []
        for n in fuente["niveles"]:
            lineas = n.get("lineas", []) + ["", "", ""]
            ing = idioma.get(str(n["nivel"]), {})
            d["niveles"].append({
                "nivel": str(n["nivel"]), "nombre": n.get("nombre", ""), "descripcion": lineas[0],
                "horas": lineas[1], "examenes": lineas[2],
                "ingles": ing.get("nombre", ""), "ingles_detalle": " · ".join(ing.get("lineas", [])),
            })
        d["verificado"] = fuente.get("verificado", True) is not False
        d.setdefault("nota", fuente.get("nota", ""))
    elif comp == "tarjetas":
        rel = Path(os.path.relpath(cfg.ruta("audios"), cfg.ruta("web"))).as_posix()
        for m in d.get("mazos", []):
            pack = por_id[m["fuente"]]
            carpeta = material(pack["id"], pack["clave"], "")
            m["tarjetas"] = [{"texto": ln["texto"], "traduccion": ln.get("traduccion", ""),
                              "audio": f"{rel}/{carpeta}/{pista_audio(pack['id'], i)}"}
                             for i, ln in enumerate(pack["lineas"], 1)]
    return d


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------

def _titulo_html(titulo: str) -> str:
    """'Tu camino a *$1000*' -> 'Tu camino a <em>$1000</em>' (escapando el resto)."""
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", html.escape(titulo))


def _plantilla() -> tuple[str, str, str]:
    base = SISTEMA / "templates" / "web"
    return tuple((base / n).read_text(encoding="utf-8") for n in ("base.html", "swa.css", "swa.js"))  # type: ignore[return-value]


def _pagina(cfg: Config, curriculo: dict[str, Any], web: dict[str, Any], titulo: str, lead: str,
            eyebrow: str, contenido: str, datos: dict[str, Any] | None) -> str:
    base, css, js = _plantilla()
    comun, marca = web.get("comun", {}), cfg["proyecto"]["marca"]
    isla = ""
    if datos is not None:
        # "</" escapado: el JSON nunca puede cerrar el <script> antes de tiempo.
        isla = ('<script type="application/json" id="swa-datos">'
                + json.dumps(datos, ensure_ascii=False).replace("</", "<\\/") + "</script>")
    reemplazos = {
        "{{TITULO}}": html.escape(re.sub(r"\*", "", titulo)),
        "{{TITULO_HTML}}": _titulo_html(titulo),
        "{{DESCRIPCION}}": html.escape(lead),
        "{{LEAD}}": html.escape(lead),
        "{{EYEBROW}}": html.escape(eyebrow),
        "{{MARCA}}": html.escape(comun.get("marca", "")),
        "{{CURSO_CORTO}}": html.escape(comun.get("curso_corto", "")),
        "{{CURSO}}": html.escape(curriculo["curso"]["titulo"]),
        "{{AUTOR}}": html.escape(cfg["proyecto"].get("autor", "")),
        "{{AVISO}}": html.escape(comun.get("aviso", "")),
        "{{PRIMARIO}}": marca["color_primario"],
        "{{SECUNDARIO}}": marca["color_secundario"],
        "{{INICIO}}": "index.html",
        "{{CSS}}": css, "{{JS}}": js, "{{DATOS}}": isla, "{{CONTENIDO}}": contenido,
    }
    for k, v in reemplazos.items():
        base = base.replace(k, v)
    return base


def _modulo(curriculo: dict[str, Any], n: int) -> dict[str, Any]:
    return next((m for m in curriculo["modulos"] if m["numero"] == n), {"numero": n, "titulo": ""})


def render_pagina(p: dict[str, Any], cfg: Config, curriculo: dict[str, Any], web: dict[str, Any],
                  mats: dict[str, Any]) -> str:
    mod = _modulo(curriculo, p.get("modulo", 0))
    eyebrow = f"Módulo {mod['numero']} · {ETIQUETA_COMPONENTE[p['componente']]}"
    datos = {"id": p["id"], "componente": p["componente"], "datos": resolver_datos(p, web, mats, cfg)}
    contenido = f'<div data-componente="{p["componente"]}"></div>'
    return _pagina(cfg, curriculo, web, p["titulo"], p.get("lead", ""), eyebrow, contenido, datos)


def render_indice(cfg: Config, curriculo: dict[str, Any], web: dict[str, Any], mats: dict[str, Any]) -> str:
    bloques = []
    for mod in curriculo["modulos"]:
        paginas = [p for p in web.get("paginas", []) if p.get("modulo") == mod["numero"]]
        pdf = cfg.ruta("workbooks") / workbook(mod["numero"])
        if not paginas and not pdf.exists():
            continue
        tarjetas = [
            f'<a class="panel item-indice" href="{material(p["id"], p["clave"], ".html")}">'
            f'<span class="chip" style="width:fit-content">{ETIQUETA_COMPONENTE[p["componente"]]}</span>'
            f'<h3>{_titulo_html(p["titulo"])}</h3><p>{html.escape(p.get("lead", ""))}</p></a>'
            for p in paginas
        ]
        if pdf.exists():
            rel = Path(os.path.relpath(pdf, cfg.ruta("web"))).as_posix()
            tarjetas.append(f'<a class="panel item-indice" href="{rel}"><span class="chip" style="width:fit-content">PDF</span>'
                            f'<h3>Workbook del módulo {mod["numero"]}</h3><p>Tareas, recursos y materiales para imprimir.</p></a>')
        bloques.append(f'<h2 class="modulo-titulo">Módulo {mod["numero"]} · {html.escape(mod["titulo"])}</h2>'
                       f'<div class="tarjetas-indice">{"".join(tarjetas)}</div>')
    return _pagina(cfg, curriculo, web, "Tus *materiales* del curso",
                   "Herramientas interactivas y workbooks para cada etapa de tu camino a Tutor PRO.",
                   curriculo["curso"]["titulo"], "".join(bloques), None)


def generar(cfg: Config, curriculo: dict[str, Any], solo: set[str] | None = None) -> list[Path]:
    web, mats = cargar(), materiales_mod.cargar()
    errores = validar(web, mats)
    if errores:
        raise ValueError("web.yaml:\n  " + "\n  ".join(errores))
    carpeta = cfg.ruta("web")
    salida = []
    for p in web.get("paginas", []):
        if solo and p["id"] not in solo:
            continue
        destino = carpeta / material(p["id"], p["clave"], ".html")
        destino.write_text(render_pagina(p, cfg, curriculo, web, mats), encoding="utf-8")
        salida.append(destino)
    indice = carpeta / "index.html"
    indice.write_text(render_indice(cfg, curriculo, web, mats), encoding="utf-8")
    salida.append(indice)
    return salida


def capturar(paginas: list[Path], navegador: str, destino: Path, tam: tuple[int, int] = (1920, 1080)) -> list[Path]:
    """PNG de cada página con el navegador en modo headless (para el video o las redes)."""
    destino.mkdir(parents=True, exist_ok=True)
    salida = []
    for p in paginas:
        png = destino / f"{p.stem}.png"
        args = [navegador, "--headless", "--disable-gpu", "--hide-scrollbars", f"--window-size={tam[0]},{tam[1]}",
                "--virtual-time-budget=4000", f"--screenshot={png}", p.resolve().as_uri()]
        if sys.platform.startswith("linux"):
            args.insert(1, "--no-sandbox")
        subprocess.run(args, check=True, capture_output=True, timeout=120)
        salida.append(png)
    return salida


def de_modulo(web: dict[str, Any], modulo: int) -> list[dict[str, Any]]:
    return [p for p in web.get("paginas", []) if p.get("modulo") == modulo]

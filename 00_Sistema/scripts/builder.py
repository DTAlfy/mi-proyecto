#!/usr/bin/env python3
"""CLI del pipeline SpanishWithAlfy Mentoring.

Flujo por lección (ejemplo M01 L01):
  ANTES DE GRABAR
    python builder.py nuevo 01 01          # esqueleto de guion (o usa /guion en Claude Code)
    python builder.py validar 01 01        # nomenclatura, etiquetas, duración
    python builder.py preparar 01 01       # dry-run de assets + teleprompter + checklist
    python builder.py preparar 01 01 --generar   # genera los assets de pago (Apimart/ElevenLabs)
  DESPUÉS DE GRABAR (02_Bruto_OBS/M01_L01_Nicho_RAW.mp4)
    python builder.py editar 01 01         # Auto-Cut + sincronización -> plan de edición
    DaVinci: Workspace > Scripts > SWA 1 - Montar leccion  ->  revisar  ->  SWA 2 - Render
  POR MÓDULO
    python builder.py workbook 01
  GLOBAL
    python builder.py estado
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from swa import assets, guion, kit, naming, visuales  # noqa: E402
from swa.config import RAIZ, SISTEMA, cargar_config, cargar_curriculo  # noqa: E402

log = logging.getLogger("swa")


def _configurar_logs(cfg) -> None:
    archivo = cfg.ruta("logs") / f"builder_{datetime.now():%Y%m%d}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[logging.FileHandler(archivo, encoding="utf-8"), logging.StreamHandler()],
    )
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def _leccion(curriculo, args) -> naming.Leccion:
    return naming.buscar_leccion(curriculo, int(args.modulo), int(args.leccion))


def _guion_validado(cfg, curriculo, lec, estricto: bool = True) -> guion.Guion:
    ruta = cfg.ruta("guiones") / lec.guion
    if not ruta.exists():
        sys.exit(f"✗ No existe {ruta.relative_to(RAIZ)}. Créalo con: builder.py nuevo {lec.modulo:02d} {lec.numero:02d}")
    g = guion.validar(guion.cargar(ruta), lec, curriculo["curso"].get("duracion_objetivo_leccion_min"))
    for a in g.avisos:
        print(f"  ⚠ {a}")
    for e in g.errores:
        print(f"  ✗ {e}")
    if g.errores and estricto:
        sys.exit(f"✗ {lec.guion}: corrige los errores antes de continuar.")
    return g


# ---------------------------------------------------------------------------
# Comandos
# ---------------------------------------------------------------------------

def cmd_validar(cfg, curriculo, args) -> None:
    errores = naming.validar_curriculo(curriculo)
    for e in errores:
        print(f"  ✗ curriculum.yaml: {e}")
    lecciones = [_leccion(curriculo, args)] if args.modulo else list(naming.iterar_lecciones(curriculo))
    total = 0
    for lec in lecciones:
        ruta = cfg.ruta("guiones") / lec.guion
        if not ruta.exists():
            if args.modulo:
                print(f"  · {lec.guion}: no existe todavía")
            continue
        print(f"{lec.guion}")
        g = _guion_validado(cfg, curriculo, lec, estricto=False)
        total += len(g.errores)
        if not g.errores:
            print(f"  ✓ {len(g.etiquetas)} etiquetas · {len(g.bloques)} bloques · ~{g.minutos_estimados:.1f} min")
    # Archivos sueltos con nombre inválido en las carpetas de ingesta
    for carpeta in ("guiones", "bruto"):
        for p in cfg.ruta(carpeta).iterdir():
            if p.is_file() and not p.name.startswith(".") and naming.analizar(p.stem) is None:
                print(f"  ✗ Nombre fuera de convención: {p.relative_to(RAIZ)}")
                total += 1
    if errores or total:
        sys.exit(1)
    print("✓ Todo válido")


def cmd_nuevo(cfg, curriculo, args) -> None:
    lec = _leccion(curriculo, args)
    destino = cfg.ruta("guiones") / lec.guion
    if destino.exists() and not args.sobrescribir:
        sys.exit(f"✗ {destino.relative_to(RAIZ)} ya existe (usa --sobrescribir)")
    plantilla = (cfg.ruta("plantillas") / "guion_plantilla.md").read_text(encoding="utf-8")
    for k, v in {"{{LECCION}}": lec.id, "{{CLAVE}}": lec.clave, "{{TITULO}}": lec.titulo,
                 "{{OBJETIVO}}": lec.objetivo, "{{MODULO_TITULO}}": lec.modulo_titulo,
                 "{{MINUTOS}}": str(curriculo["curso"].get("duracion_objetivo_leccion_min", 8))}.items():
        plantilla = plantilla.replace(k, v)
    destino.write_text(plantilla, encoding="utf-8")
    print(f"✓ Creado {destino.relative_to(RAIZ)}")


def cmd_assets(cfg, curriculo, args) -> None:
    lec = _leccion(curriculo, args)
    g = _guion_validado(cfg, curriculo, lec)
    plan = assets.planificar(g, lec, cfg)
    print(f"\nAssets de {lec.base} ({'GENERAR' if args.generar else 'dry-run'}):")
    try:
        assets.generar(plan, cfg, curriculo, lec, dry_run=not args.generar,
                       forzar_presupuesto=args.forzar_presupuesto)
    except RuntimeError as e:
        sys.exit(f"✗ {e}")


def cmd_kit(cfg, curriculo, args) -> None:
    lec = _leccion(curriculo, args)
    g = _guion_validado(cfg, curriculo, lec)
    plan = assets.planificar(g, lec, cfg)
    # Los visuales locales son gratis: se generan siempre para que el checklist los vea.
    assets.generar([i for i in plan if i.es_local], cfg, curriculo, lec, dry_run=False, informar=lambda _: None)
    tp = kit.teleprompter(g, lec, cfg)
    cl = kit.checklist(g, lec, cfg, plan)
    print(f"✓ Teleprompter: {tp.relative_to(RAIZ)}")
    print(f"✓ Checklist:    {cl.relative_to(RAIZ)}")


def cmd_preparar(cfg, curriculo, args) -> None:
    cmd_assets(cfg, curriculo, args)
    print()
    cmd_kit(cfg, curriculo, args)


def cmd_editar(cfg, curriculo, args) -> None:
    from swa import autocut, edicion
    lec = _leccion(curriculo, args)
    g = _guion_validado(cfg, curriculo, lec)
    raw = next((cfg.ruta("bruto") / lec.archivo("RAW", ext) for ext in naming.EXT_RAW
                if (cfg.ruta("bruto") / lec.archivo("RAW", ext)).exists()), None)
    if raw is None:
        sys.exit(f"✗ No encuentro {lec.archivo('RAW', '.mp4')} (o .mkv/.mov) en {cfg['rutas']['bruto']}/")

    transcripcion = None
    if cfg["proveedores"].get("transcripcion", "ninguno") != "ninguno" and not args.sin_transcripcion:
        cache = cfg.ruta("ediciones") / f"{lec.base}_TRANSCRIPCION.json"
        if cache.exists():
            transcripcion = json.loads(cache.read_text(encoding="utf-8"))
            print("  · Transcripción reutilizada de caché (no se paga de nuevo)")
        else:
            from swa.providers.apimart import Apimart
            audio = cfg.ruta("ediciones") / f"{lec.base}_audio.mp3"
            print("  · Extrayendo audio ligero y transcribiendo…")
            autocut.extraer_audio_ligero(raw, audio, cfg["autocut"]["ffmpeg"])
            try:
                transcripcion = Apimart(cfg["apimart"]).transcribir(audio)
                cache.write_text(json.dumps(transcripcion, ensure_ascii=False), encoding="utf-8")
            except Exception as e:  # la transcripción es una mejora, no un requisito
                print(f"  ⚠ Transcripción no disponible ({e}). Se usará estimación por palabras.")
            finally:
                audio.unlink(missing_ok=True)

    plan_assets = assets.planificar(g, lec, cfg)
    plan = edicion.construir(g, lec, cfg, plan_assets, raw, transcripcion)
    destino = edicion.guardar(plan, cfg, lec)
    print(f"✓ Plan de edición: {destino.relative_to(RAIZ)}")
    print(f"  {len(plan['segmentos'])} tramos · {plan['duracion_raw_s']:.0f}s → {plan['duracion_final_s']:.0f}s · "
          f"{len(plan['inserciones'])} inserciones · sincronización: {plan['metodo_sincronizacion']}")
    print("  Siguiente: DaVinci › Workspace › Scripts › SWA 1 - Montar leccion")


def cmd_workbook(cfg, curriculo, args) -> None:
    from swa import workbook
    modulo = int(args.modulo)
    roadmap = cfg.ruta("assets") / "ROADMAP" / f"M{modulo:02d}_Roadmap.png"
    visuales.roadmap(curriculo, modulo, roadmap, cfg["proyecto"]["marca"])
    destino, avisos = workbook.generar(modulo, cfg, curriculo, solo_html=args.solo_html)
    for a in avisos:
        print(f"  ⚠ {a}")
    print(f"✓ Workbook: {destino.relative_to(RAIZ)}")


def cmd_roadmap(cfg, curriculo, args) -> None:
    for mod in curriculo["modulos"]:
        destino = cfg.ruta("assets") / "ROADMAP" / f"M{mod['numero']:02d}_Roadmap.png"
        visuales.roadmap(curriculo, mod["numero"], destino, cfg["proyecto"]["marca"])
        print(f"✓ {destino.relative_to(RAIZ)}")


def cmd_estado(cfg, curriculo, args) -> None:
    manifest_ok = assets.cargar_manifest(cfg)
    cab = f"{'Lección':<28} {'Guion':^6} {'Assets':^8} {'Kit':^4} {'RAW':^4} {'Edic.':^6} {'FINAL':^6}"
    print(cab + "\n" + "─" * len(cab))
    for lec in naming.iterar_lecciones(curriculo):
        ruta_g = cfg.ruta("guiones") / lec.guion
        col_assets = "·"
        if ruta_g.exists():
            g = guion.cargar(ruta_g)
            plan = assets.planificar(g, lec, cfg)
            listos = sum(1 for i in plan if i.destino.exists())
            col_assets = f"{listos}/{len(plan)}"
        marca = lambda p: "✓" if p.exists() else "·"  # noqa: E731
        raw = any((cfg.ruta("bruto") / lec.archivo("RAW", e)).exists() for e in naming.EXT_RAW)
        print(f"{lec.base:<28} {marca(ruta_g):^6} {col_assets:^8} "
              f"{marca(cfg.ruta('teleprompter') / lec.archivo('TELEPROMPTER', '.html')):^4} "
              f"{'✓' if raw else '·':^4} "
              f"{marca(cfg.ruta('ediciones') / lec.archivo('EDICION', '.json')):^6} "
              f"{marca(cfg.ruta('renders') / lec.archivo('FINAL', '.mp4')):^6}")
    print(f"\nAssets pagados en caché: {len(manifest_ok)}")


def cmd_instalar_davinci(cfg, curriculo, args) -> None:
    """Copia lanzadores a la carpeta de scripts de Resolve. Apuntan al repo: no hay que reinstalar al actualizar."""
    if args.destino:
        destino = Path(args.destino)
    elif sys.platform == "win32":
        destino = Path(os.environ["APPDATA"]) / "Blackmagic Design/DaVinci Resolve/Support/Fusion/Scripts/Edit"
    elif sys.platform == "darwin":
        destino = Path.home() / "Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Edit"
    else:
        destino = Path.home() / ".local/share/DaVinciResolve/Fusion/Scripts/Edit"
    destino.mkdir(parents=True, exist_ok=True)
    scripts = SISTEMA / "scripts" / "resolve"
    for nombre, real in (("SWA 1 - Montar leccion.py", "swa_montar.py"), ("SWA 2 - Render.py", "swa_render.py")):
        (destino / nombre).write_text(
            "# Lanzador generado por builder.py instalar-davinci. No editar: el código vive en el repo.\n"
            "import runpy\n"
            f"runpy.run_path({str(scripts / real)!r}, init_globals=globals())\n",
            encoding="utf-8",
        )
        print(f"✓ {destino / nombre}")
    print("Reinicia DaVinci Resolve y búscalos en Workspace › Scripts.")


def cmd_comparar_voces(cfg, curriculo, args) -> None:
    """Genera la misma frase con ElevenLabs y Apimart para elegir de oído (2 llamadas de pago)."""
    from swa.providers.apimart import Apimart
    from swa.providers.elevenlabs import ElevenLabs
    carpeta = cfg.ruta("assets") / "AUDIO" / "_comparacion"
    carpeta.mkdir(parents=True, exist_ok=True)
    for nombre, cliente in (("elevenlabs", ElevenLabs(cfg["elevenlabs"])), ("apimart", Apimart(cfg["apimart"]))):
        try:
            (carpeta / f"{nombre}.mp3").write_bytes(cliente.tts(args.frase))
            print(f"✓ {(carpeta / f'{nombre}.mp3').relative_to(RAIZ)}")
        except Exception as e:
            print(f"✗ {nombre}: {e}")


# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="builder.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    def con_leccion(nombre: str, ayuda: str, opcional: bool = False) -> argparse.ArgumentParser:
        sp = sub.add_parser(nombre, help=ayuda)
        sp.add_argument("modulo", nargs="?" if opcional else None, help="Número de módulo, ej. 01")
        sp.add_argument("leccion", nargs="?" if opcional else None, help="Número de lección, ej. 01")
        return sp

    con_leccion("validar", "Valida currículo y guiones (todos o uno)", opcional=True)
    con_leccion("nuevo", "Crea el esqueleto de guion desde la plantilla").add_argument("--sobrescribir", action="store_true")
    for nombre, ayuda in (("assets", "Planifica/genera assets de una lección"),
                          ("preparar", "assets + kit: todo lo necesario para grabar")):
        sp = con_leccion(nombre, ayuda)
        sp.add_argument("--generar", action="store_true", help="Gasta saldo de verdad (sin esto: dry-run)")
        sp.add_argument("--forzar-presupuesto", action="store_true")
    con_leccion("kit", "Teleprompter + checklist + slides/roadmap locales")
    con_leccion("editar", "Auto-Cut + sincronización -> plan para DaVinci").add_argument(
        "--sin-transcripcion", action="store_true", help="No transcribir: coloca visuales por estimación")
    wb = sub.add_parser("workbook", help="Genera el workbook PDF de un módulo")
    wb.add_argument("modulo")
    wb.add_argument("--solo-html", action="store_true")
    sub.add_parser("roadmap", help="Regenera las imágenes del Roadmap de Ingresos")
    sub.add_parser("estado", help="Tabla de avance de todas las lecciones")
    sub.add_parser("instalar-davinci", help="Instala los scripts en DaVinci Resolve").add_argument("--destino")
    sub.add_parser("comparar-voces", help="Misma frase con ElevenLabs y Apimart").add_argument("frase")

    for flujo in (sys.stdout, sys.stderr):  # consola de Windows: que los ✓ y las tildes no rompan
        if hasattr(flujo, "reconfigure"):
            flujo.reconfigure(encoding="utf-8", errors="replace")
    args = p.parse_args(argv)
    if args.cmd == "validar" and bool(args.modulo) != bool(args.leccion):
        p.error("validar: indica módulo Y lección, o ninguno")
    cfg = cargar_config()
    _configurar_logs(cfg)
    curriculo = cargar_curriculo()
    globals()["cmd_" + args.cmd.replace("-", "_")](cfg, curriculo, args)


if __name__ == "__main__":
    main()

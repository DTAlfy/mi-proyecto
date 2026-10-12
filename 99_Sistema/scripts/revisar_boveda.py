#!/usr/bin/env python3
"""Revisa una bóveda de Obsidian: inventario, conexiones y enlaces rotos.

Sirve para organizar con datos: muestra qué hay en cada carpeta, qué carpetas están
aisladas (las "estrellas" sueltas del grafo), cuáles son las notas centrales (hubs)
y qué enlaces se rompen al mover cosas.

Uso:
  python 99_Sistema/scripts/revisar_boveda.py                       inventario de esta bóveda
  python 99_Sistema/scripts/revisar_boveda.py --boveda "C:/ruta/Second Brain"
  python 99_Sistema/scripts/revisar_boveda.py --enlaces             solo enlaces rotos (sale con código 1 si hay)
  python 99_Sistema/scripts/revisar_boveda.py --salida informe.md   guarda el informe en un archivo
"""
import argparse
import posixpath
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import unquote

import boveda as bv

IGNORAR = {".obsidian", ".git", ".trash", "node_modules", "__pycache__"}
WIKI = re.compile(r"!?\[\[([^\]|#^]*)(?:[#^][^\]|]*)?(?:\|[^\]]*)?\]\]")
MD = re.compile(r"!?\[[^\]]*\]\(([^)\s]+\.md)(?:#[^)]*)?\)")
FENCE = re.compile(r"```.*?```|`[^`\n]*`", re.S)


def archivos(raiz):
    for p in sorted(raiz.rglob("*")):
        rel = p.relative_to(raiz)
        if p.is_file() and not (set(rel.parts) & IGNORAR) and not p.name.startswith("."):
            yield p, rel


def analizar(raiz):
    todos = list(archivos(raiz))
    notas = [(p, r) for p, r in todos if p.suffix.lower() == ".md"]
    por_nombre = defaultdict(list)   # "nombre" (sin .md) o "archivo.ext" -> rutas relativas sin extensión
    por_ruta = {}
    for p, r in todos:
        clave = r.with_suffix("").as_posix() if p.suffix.lower() == ".md" else r.as_posix()
        por_ruta[clave.lower()] = clave
        por_nombre[(p.stem if p.suffix.lower() == ".md" else p.name).lower()].append(clave)

    def resolver(destino, origen):
        d = unquote(destino).strip().rstrip("\\").replace("\\", "/")
        if not d:
            return "vacío"
        if d.lower().endswith(".md"):
            d = d[:-3]
        if "/" in d:
            d_rel = posixpath.normpath(posixpath.join(posixpath.dirname(origen), d))
            for cand in (d.lstrip("/").lower(), d_rel.lower()):
                if cand in por_ruta:
                    return por_ruta[cand]
            fin = [v for k, v in por_ruta.items() if k.endswith("/" + d.lower())]
            return fin[0] if fin else None
        cands = por_nombre.get(d.lower())
        return cands[0] if cands else None

    salientes, entrantes, rotos = defaultdict(set), Counter(), []
    con_props = con_tipo = 0
    tipos = Counter()
    for p, r in notas:
        texto = p.read_text(encoding="utf-8", errors="replace")
        props, cuerpo = bv.separar(texto)
        if props:
            con_props += 1
        if props.get("tipo"):
            con_tipo += 1
            tipos[str(props["tipo"])] += 1
        origen = r.with_suffix("").as_posix()
        limpio = FENCE.sub("", texto)
        for destino in WIKI.findall(limpio) + MD.findall(limpio):
            if destino.startswith(("http://", "https://")):
                continue
            res = resolver(destino, r.as_posix())
            if res == "vacío":
                continue
            if res is None:
                rotos.append((r.as_posix(), destino))
            elif res != origen:
                salientes[origen].add(res)
    for o, ds in salientes.items():
        for d in ds:
            entrantes[d] += 1
    return todos, notas, salientes, entrantes, rotos, con_props, con_tipo, tipos


def carpeta(ruta):
    partes = ruta.split("/")
    return partes[0] if len(partes) > 1 else "(raíz)"


def informe(raiz, todos, notas, salientes, entrantes, rotos, con_props, con_tipo, tipos):
    n = len(notas)
    lineas = [f"# Inventario de la bóveda", "", f"Ruta: `{raiz}`", "",
              "## Resumen", "",
              f"- Notas `.md`: **{n}** · otros archivos: **{len(todos) - n}**",
              f"- Con propiedades (frontmatter): **{con_props}** ({round(100 * con_props / n) if n else 0} %)"
              f" · con `tipo`: **{con_tipo}** ({round(100 * con_tipo / n) if n else 0} %)",
              f"- Enlaces entre notas: **{sum(len(v) for v in salientes.values())}** · enlaces rotos: **{len(rotos)}**"]
    huerfanas = [r.with_suffix("").as_posix() for _, r in notas
                 if not salientes.get(r.with_suffix("").as_posix()) and not entrantes.get(r.with_suffix("").as_posix())]
    lineas.append(f"- Notas huérfanas (sin enlaces de entrada ni salida): **{len(huerfanas)}**")
    if tipos:
        lineas += ["", "Tipos: " + " · ".join(f"`{t}` {c}" for t, c in tipos.most_common())]

    lineas += ["", "## Carpetas", "",
               "*Salen fuera* = % de sus enlaces que van a **otra** carpeta. *Entran de fuera* = enlaces que recibe desde otras carpetas.",
               "Una carpeta con ~0 % hacia fuera y 0 entrantes está **aislada** (una \"estrella\" suelta en el grafo).", "",
               "| Carpeta | Notas | Otros archivos | Tipos de archivo | Enlaces | Salen fuera | Entran de fuera |",
               "|---|---|---|---|---|---|---|"]
    stats = defaultdict(lambda: {"notas": 0, "otros": 0, "ext": Counter(), "enl": 0, "fuera": 0, "entran": 0})
    for p, r in todos:
        s = stats[carpeta(r.as_posix())]
        if p.suffix.lower() == ".md":
            s["notas"] += 1
        else:
            s["otros"] += 1
            s["ext"][p.suffix.lower() or "(sin ext)"] += 1
    for o, ds in salientes.items():
        for d in ds:
            s = stats[carpeta(o)]
            s["enl"] += 1
            if carpeta(d) != carpeta(o):
                s["fuera"] += 1
                stats[carpeta(d)]["entran"] += 1
    for c in sorted(stats):
        s = stats[c]
        pct = f"{round(100 * s['fuera'] / s['enl'])} %" if s["enl"] else "—"
        aviso = " ⚠️ aislada" if s["enl"] >= 20 and s["fuera"] / s["enl"] < 0.05 and s["entran"] == 0 else ""
        ext = ", ".join(f"{e} {k}" for e, k in s["ext"].most_common(4))
        lineas.append(f"| `{c}` | {s['notas']} | {s['otros']} | {ext} | {s['enl']} | {pct} | {s['entran']}{aviso} |")

    lineas += ["", "## Notas centrales (hubs)", "", "Las que más enlaces tienen: suelen ser el índice de un libro o un mapa.", "",
               "| Nota | Enlaces que salen | Enlaces que entran |", "|---|---|---|"]
    hubs = sorted(salientes, key=lambda k: -(len(salientes[k]) + entrantes[k]))[:15]
    lineas += [f"| `{h}` | {len(salientes[h])} | {entrantes[h]} |" for h in hubs] or ["| — | — | — |"]

    lineas += ["", f"## Enlaces rotos ({len(rotos)})", ""]
    lineas += [f"- `{o}` → `[[{d}]]`" for o, d in rotos[:50]] or ["- Ninguno ✅"]
    if len(rotos) > 50:
        lineas.append(f"- … y {len(rotos) - 50} más (usa `--enlaces` para verlos todos)")
    lineas += ["", f"## Huérfanas ({len(huerfanas)})", ""]
    lineas += [f"- `{h}`" for h in huerfanas[:30]] or ["- Ninguna"]
    if len(huerfanas) > 30:
        lineas.append(f"- … y {len(huerfanas) - 30} más")
    return "\n".join(lineas) + "\n"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--boveda", default=str(Path(__file__).resolve().parents[2]), help="Raíz de la bóveda")
    parser.add_argument("--enlaces", action="store_true", help="Listar solo los enlaces rotos")
    parser.add_argument("--salida", help="Guardar el informe en este archivo")
    args = parser.parse_args()
    raiz = Path(args.boveda)
    datos = analizar(raiz)
    rotos = datos[4]
    if args.enlaces:
        for o, d in rotos:
            print(f"{o} → [[{d}]]")
        print(f"{len(rotos)} enlaces rotos")
        return 1 if rotos else 0
    texto = informe(raiz, *datos)
    if args.salida:
        Path(args.salida).write_text(texto, encoding="utf-8")
        print(f"Informe guardado en {args.salida}")
    else:
        print(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main())

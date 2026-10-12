#!/usr/bin/env python3
"""Árbol de habilidades: calcula el progreso de cada alumno y genera sus árboles.

Lee:
  30_Curriculum/Arbol/**      nodos (situaciones, gramática, vocabulario) con `requiere:`
  40_Clases/Materiales/**     materiales con `nodos:` (aparecen al desbloquear el nodo)
  60_Estudiantes/Alumnos/     fichas (`nivel_base`, `dominados`, `meta`)
  60_Estudiantes/Sesiones/    sesiones (`practicados`, `logrados`)
  60_Estudiantes/Evaluaciones evaluaciones (`logrados`)

Genera:
  30_Curriculum/Arbol maestro.html / .canvas       el árbol completo
  60_Estudiantes/Arboles/<Alumno>.html / .canvas    el árbol de cada alumno
  60_Estudiantes/Arboles/<Alumno> - Ruta.md         qué puede hacer, qué sigue, ruta a su meta
  60_Estudiantes/Arboles/Panel de progreso.md       métricas de todos los alumnos

Uso (desde cualquier carpeta):
  python 99_Sistema/scripts/arbol.py               genera todo
  python 99_Sistema/scripts/arbol.py --validar     solo revisa el árbol (enlaces rotos, ciclos…)
  python 99_Sistema/scripts/arbol.py --alumno "Nombre Apellido"
"""
import argparse
import heapq
import html
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

import boveda as bv

ARBOL = "30_Curriculum/Arbol"
MATERIALES = "40_Clases/Materiales"
ALUMNOS = "60_Estudiantes/Alumnos"
SESIONES = "60_Estudiantes/Sesiones"
EVALUACIONES = "60_Estudiantes/Evaluaciones"
SALIDA_ALUMNOS = "60_Estudiantes/Arboles"
MAESTRO = "30_Curriculum/Arbol maestro"

RAMAS = ["vocabulario", "gramatica", "situacion"]
CARRILES = ["situacion", "gramatica", "vocabulario"]  # orden de columnas en el dibujo
RAMA_NOMBRE = {"vocabulario": "Vocabulario", "gramatica": "Gramática", "situacion": "Situaciones"}
ESTADOS_VISIBLES = {"dominado", "en_curso", "disponible", "proximo"}
ICONO = {"dominado": "✅", "en_curso": "🟡", "disponible": "🔓", "proximo": "🔒", "bloqueado": "⬛"}
UMBRAL_NIVEL = 80  # % de nodos dominados para dar un nivel por completado

# Disposición del árbol (píxeles en el HTML)
W, H, GX, GY = 196, 58, 12, 14
COLS = 2
MARGEN, CABECERA, SEP_BANDA, SEP_CARRIL = 24, 40, 20, 36


# ---------------------------------------------------------------- carga

def _mision_y_goals(cuerpo):
    m = re.search(r"\*\*Misión:\*\*\s*(.+)", cuerpo)
    mision = m.group(1).strip() if m else ""
    goals, dentro = [], False
    for linea in cuerpo.splitlines():
        if linea.startswith("## "):
            dentro = linea.lower().startswith("## goals")
            continue
        g = re.match(r"\s*- \[[ xX]\]\s*(.+)", linea)
        if dentro and g:
            goals.append(g.group(1).strip())
    return mision, goals


def cargar_arbol(raiz):
    nodos, avisos, errores = {}, [], []
    for ruta in sorted((raiz / ARBOL).rglob("*.md")):
        props, cuerpo = bv.leer(ruta)
        if props.get("tipo") != "nodo":
            continue
        codigo = props.get("codigo") or ruta.stem.split(" ")[0]
        mision, goals = _mision_y_goals(cuerpo)
        nodos[ruta.stem] = {
            "id": ruta.stem,
            "codigo": codigo,
            "titulo": ruta.stem[len(codigo):].strip() if ruta.stem.startswith(codigo) else ruta.stem,
            "nivel": props.get("nivel", ""),
            "rama": props.get("rama", ""),
            "req_texto": bv.enlaces(props.get("requiere")),
            "estado_nota": props.get("estado", ""),
            "ruta": ruta.relative_to(raiz).as_posix(),
            "mision": mision,
            "goals": goals,
            "materiales": [],
        }
    por_codigo = {n["codigo"]: n["id"] for n in nodos.values()}

    def resolver(nombre):
        if nombre in nodos:
            return nombre
        return por_codigo.get(nombre.split(" ")[0])

    for n in nodos.values():
        n["requiere"] = []
        for r in n["req_texto"]:
            destino = resolver(r)
            if destino:
                n["requiere"].append(destino)
            else:
                errores.append(f"{n['id']}: requisito no encontrado → [[{r}]]")
        if n["nivel"] not in bv.NIVELES:
            errores.append(f"{n['id']}: nivel inválido '{n['nivel']}'")
        if n["rama"] not in RAMAS:
            errores.append(f"{n['id']}: rama inválida '{n['rama']}' (usa {', '.join(RAMAS)})")
        for r in n["requiere"]:
            if bv.indice_nivel(nodos[r]["nivel"]) > bv.indice_nivel(n["nivel"]):
                avisos.append(f"{n['id']}: requiere un nodo de nivel superior → {r}")
    errores += [f"Ciclo de requisitos: {' → '.join(c)}" for c in _ciclos(nodos)]

    for ruta in sorted((raiz / MATERIALES).rglob("*.md")):
        props, _ = bv.leer(ruta)
        if props.get("tipo") != "material":
            continue
        for destino in bv.enlaces(props.get("nodos")):
            nodo = resolver(destino)
            if nodo:
                nodos[nodo]["materiales"].append({"titulo": ruta.stem, "ruta": ruta.relative_to(raiz).as_posix(),
                                                  "formato": props.get("formato", "")})
            else:
                avisos.append(f"{ruta.stem}: material enlazado a un nodo que no existe → [[{destino}]]")
    return nodos, resolver, avisos, errores


def _ciclos(nodos):
    color, pila, ciclos = {}, [], []

    def visitar(n):
        color[n] = 1
        pila.append(n)
        for r in nodos[n]["requiere"]:
            if color.get(r) == 1:
                ciclos.append(pila[pila.index(r):] + [r])
            elif r not in color:
                visitar(r)
        pila.pop()
        color[n] = 2

    for n in nodos:
        if n not in color:
            visitar(n)
    return ciclos


def cargar_alumnos(raiz, resolver, avisos):
    alumnos = {}
    for ruta in sorted((raiz / ALUMNOS).glob("*.md")):
        props, _ = bv.leer(ruta)
        if props.get("tipo") == "alumno":
            alumnos[ruta.stem] = {"nombre": ruta.stem, "props": props, "logros": {}, "practicas": {},
                                  "sesiones": 0, "ultima": ""}
    for carpeta in (SESIONES, EVALUACIONES):
        for ruta in sorted((raiz / carpeta).glob("*.md")):
            props, _ = bv.leer(ruta)
            tipo = props.get("tipo")
            if tipo not in ("sesion", "evaluacion"):
                continue
            quien = bv.enlaces(props.get("alumno"))
            if not quien or quien[0] not in alumnos:
                avisos.append(f"{ruta.stem}: el alumno enlazado no tiene ficha → {quien[0] if quien else '(vacío)'}")
                continue
            a = alumnos[quien[0]]
            fecha = str(props.get("fecha", ""))
            if tipo == "sesion":
                a["sesiones"] += 1
                a["ultima"] = max(a["ultima"], fecha)
            for clave, destino_dict in (("practicados", a["practicas"]), ("logrados", a["practicas"])):
                for n in bv.enlaces(props.get(clave)):
                    nodo = resolver(n)
                    if nodo:
                        destino_dict.setdefault(nodo, set()).add(fecha)
                    else:
                        avisos.append(f"{ruta.stem}: nodo no encontrado en '{clave}' → [[{n}]]")
            for n in bv.enlaces(props.get("logrados")):
                nodo = resolver(n)
                if nodo:
                    previo = a["logros"].get(nodo)
                    a["logros"][nodo] = min(previo, fecha) if previo else fecha
    return alumnos


# ---------------------------------------------------------------- cálculo

def niveles_presentes(nodos):
    return [nv for nv in bv.NIVELES if any(n["nivel"] == nv for n in nodos.values())]


def calcular(alumno, nodos, resolver, hoy):
    props = alumno["props"]
    base = bv.indice_nivel(props.get("nivel_base", ""))
    dominados = dict(alumno["logros"])
    for n in nodos.values():
        if base >= 0 and bv.indice_nivel(n["nivel"]) <= base:
            dominados.setdefault(n["id"], "base")
    for d in bv.enlaces(props.get("dominados")):
        if resolver(d):
            dominados.setdefault(resolver(d), "ficha")

    estado, faltan = {}, {}
    for n in nodos.values():
        faltan[n["id"]] = [r for r in n["requiere"] if r not in dominados]
        if n["id"] in dominados:
            estado[n["id"]] = "dominado"
        elif n["id"] in alumno["practicas"]:
            estado[n["id"]] = "en_curso"
        elif not faltan[n["id"]]:
            estado[n["id"]] = "disponible"
        else:
            estado[n["id"]] = "bloqueado"
    for nid, e in list(estado.items()):
        if e == "bloqueado" and all(estado[f] in ("disponible", "en_curso") for f in faltan[nid]):
            estado[nid] = "proximo"

    por_nivel = []
    for nv in niveles_presentes(nodos):
        total = [n for n in nodos.values() if n["nivel"] == nv]
        dom = sum(1 for n in total if estado[n["id"]] == "dominado")
        por_nivel.append({"nivel": nv, "dominados": dom, "total": len(total), "pct": round(100 * dom / len(total))})
    completado, trabajando = "", por_nivel[0]["nivel"] if por_nivel else ""
    for i, fila in enumerate(por_nivel):
        if fila["pct"] < UMBRAL_NIVEL:
            trabajando = fila["nivel"]
            break
        completado = fila["nivel"]
        trabajando = por_nivel[i + 1]["nivel"] if i + 1 < len(por_nivel) else fila["nivel"]
    progreso = next((f["pct"] for f in por_nivel if f["nivel"] == trabajando), 0)

    meta = next((resolver(m) for m in bv.enlaces(props.get("meta")) if resolver(m)), None)
    ruta = _ruta(meta, nodos, dominados) if meta else []

    hijos = {}
    for n in nodos.values():
        for r in n["requiere"]:
            hijos.setdefault(r, []).append(n["id"])
    en_ruta = set(ruta)
    candidatos = [nid for nid, e in estado.items() if e in ("disponible", "en_curso")]

    def impacto(nid):
        return sum(1 for h in hijos.get(nid, []) if estado[h] != "dominado")

    def clave(nid):
        n = nodos[nid]
        return (estado[nid] != "en_curso", nid not in en_ruta, bv.indice_nivel(n["nivel"]),
                n["rama"] != "situacion", -impacto(nid), n["codigo"])

    siguiente = []
    for nid in sorted(candidatos, key=clave)[:3]:
        motivos = []
        if nid in en_ruta:
            motivos.append("está en la ruta hacia su meta")
        if estado[nid] == "en_curso":
            motivos.append("ya lo está practicando")
        if nodos[nid]["rama"] == "situacion":
            motivos.append("situación lista para practicar")
        if impacto(nid):
            motivos.append(f"desbloquea {impacto(nid)} nodo(s)")
        siguiente.append({"id": nid, "motivo": ", ".join(motivos) or "disponible"})

    desde = (hoy - timedelta(days=30)).isoformat()
    recientes = sum(1 for f in alumno["logros"].values() if f >= desde)
    return {
        "estado": estado, "faltan": faltan, "dominados": dominados, "por_nivel": por_nivel,
        "completado": completado, "trabajando": trabajando, "progreso": progreso,
        "meta": meta, "ruta": ruta, "siguiente": siguiente, "recientes": recientes,
    }


def _ruta(meta, nodos, dominados):
    """Nodos pendientes hasta la meta, en un orden que respeta los requisitos."""
    pendientes, pila = set(), [meta]
    while pila:
        n = pila.pop()
        if n in pendientes or n in dominados:
            continue
        pendientes.add(n)
        pila.extend(nodos[n]["requiere"])
    grado = {n: sum(1 for r in nodos[n]["requiere"] if r in pendientes) for n in pendientes}

    def prioridad(n):
        return (bv.indice_nivel(nodos[n]["nivel"]), RAMAS.index(nodos[n]["rama"]) if nodos[n]["rama"] in RAMAS else 9,
                nodos[n]["codigo"])

    cola = [(prioridad(n), n) for n in pendientes if grado[n] == 0]
    heapq.heapify(cola)
    orden = []
    while cola:
        _, n = heapq.heappop(cola)
        orden.append(n)
        for m in pendientes:
            if n in nodos[m]["requiere"]:
                grado[m] -= 1
                if grado[m] == 0:
                    heapq.heappush(cola, (prioridad(m), m))
    return orden


def sesiones_hasta_dominar(alumnos):
    """Por nodo: cuántas sesiones hicieron falta de media hasta lograrlo (para optimizar materiales)."""
    datos = {}
    for a in alumnos.values():
        for nodo, fecha_logro in a["logros"].items():
            n_ses = len([f for f in a["practicas"].get(nodo, set()) if f <= fecha_logro]) or 1
            datos.setdefault(nodo, []).append(n_ses)
    return {n: (sum(v) / len(v), len(v)) for n, v in datos.items()}


# ---------------------------------------------------------------- disposición

def disponer(nodos):
    ancho_carril = COLS * W + (COLS - 1) * GX
    x_carril = {r: MARGEN + i * (ancho_carril + SEP_CARRIL) for i, r in enumerate(CARRILES)}
    pos, bandas, y = {}, [], MARGEN
    for nv in niveles_presentes(nodos):
        filas = 1
        for rama in CARRILES:
            del_carril = sorted((n for n in nodos.values() if n["nivel"] == nv and n["rama"] == rama),
                                key=lambda n: n["codigo"])
            for i, n in enumerate(del_carril):
                pos[n["id"]] = (x_carril[rama] + (i % COLS) * (W + GX), y + CABECERA + (i // COLS) * (H + GY))
            filas = max(filas, -(-len(del_carril) // COLS))
        alto = CABECERA + filas * (H + GY) + 6
        bandas.append({"nivel": nv, "y": y, "h": alto})
        y += alto + SEP_BANDA
    ancho = 2 * MARGEN + len(CARRILES) * ancho_carril + (len(CARRILES) - 1) * SEP_CARRIL
    carriles = [{"rama": r, "x": x_carril[r], "nombre": RAMA_NOMBRE[r]} for r in CARRILES]
    return pos, bandas, carriles, ancho, y + MARGEN


# ---------------------------------------------------------------- salidas

def datos_html(nodos, pos, bandas, carriles, ancho, alto, calc=None):
    lista = []
    for n in nodos.values():
        if n["id"] not in pos:
            continue
        x, y = pos[n["id"]]
        item = {k: n[k] for k in ("id", "codigo", "titulo", "nivel", "rama", "requiere", "mision", "goals",
                                  "materiales", "ruta")}
        item.update(x=x, y=y)
        if calc:
            item["estado"] = calc["estado"][n["id"]]
            item["faltan"] = calc["faltan"][n["id"]]
            logro = calc["dominados"].get(n["id"])
            item["logro"] = logro if logro not in ("base", "ficha") else ""
            item["en_ruta"] = n["id"] in calc["ruta"]
        lista.append(item)
    return {"nodos": lista, "bandas": bandas, "carriles": carriles, "ancho": ancho, "alto": alto,
            "W": W, "H": H}


def escribir_html(ruta, titulo, subtitulo, datos):
    datos = dict(datos, titulo=titulo, subtitulo=subtitulo)
    js = json.dumps(datos, ensure_ascii=False).replace("</", "<\\/")
    contenido = PLANTILLA_HTML.replace("__TITULO__", html.escape(titulo)).replace("__DATOS__", js)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(contenido, encoding="utf-8")


def escribir_canvas(ruta, nodos, pos, bandas, calc=None):
    sx, sy = 1.4, 1.75
    color_rama = {"situacion": "2", "gramatica": "6", "vocabulario": "5"}
    color_estado = {"dominado": "4", "en_curso": "3", "disponible": "5"}
    ids = {nid: "n_" + re.sub(r"\W", "_", nodos[nid]["codigo"]) for nid in pos}
    elementos, aristas = [], []
    ancho_total = int(max(x for x, _ in pos.values()) * sx + W * sx + 40)
    for b in bandas:
        elementos.append({"id": f"banda_{b['nivel']}", "type": "group", "label": b["nivel"],
                          "x": int(MARGEN * sx) - 30, "y": int(b["y"] * sy), "width": ancho_total,
                          "height": int(b["h"] * sy)})
    for nid, (x, y) in pos.items():
        n = nodos[nid]
        estado = calc["estado"][nid] if calc else None
        texto = f"[[{nid}]]" if not calc else f"{ICONO[estado]} [[{nid}]]"
        elem = {"id": ids[nid], "type": "text", "text": texto, "x": int(x * sx), "y": int(y * sy),
                "width": int(W * sx), "height": int(H * sy)}
        color = color_estado.get(estado) if calc else color_rama.get(n["rama"])
        if color:
            elem["color"] = color
        elementos.append(elem)
        for r in n["requiere"]:
            if r in ids:
                aristas.append({"id": f"e_{ids[r]}_{ids[nid]}", "fromNode": ids[r], "toNode": ids[nid]})
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps({"nodes": elementos, "edges": aristas}, ensure_ascii=False, indent=1),
                    encoding="utf-8")


def escribir_ruta_md(ruta, alumno, nodos, calc, hoy):
    p, est = alumno["props"], calc["estado"]
    enl = lambda nid: f"[[{nid}]]"
    situaciones_dom = [n for n in nodos if est[n] == "dominado" and nodos[n]["rama"] == "situacion"]
    meta_txt = enl(calc["meta"]) if calc["meta"] else ""
    lineas = [
        "---", "tipo: ruta", f'alumno: "[[{alumno["nombre"]}]]"', f"estado_alumno: {p.get('estado', '')}",
        f"nivel_completado: {calc['completado'] or 'ninguno'}", f"nivel_en_curso: {calc['trabajando']}",
        f"progreso: {calc['progreso']}", f"dominados: {sum(1 for e in est.values() if e == 'dominado')}",
        f"disponibles: {sum(1 for e in est.values() if e == 'disponible')}",
        f"logrados_30d: {calc['recientes']}", f"sesiones: {alumno['sesiones']}",
        f"ultima_sesion: {alumno['ultima']}", f'meta: "{meta_txt}"', f"pasos_hasta_meta: {len(calc['ruta'])}",
        f"actualizado: {hoy.isoformat()}", "---",
        f"# Ruta de {alumno['nombre']}", "",
        "> Generado por `99_Sistema/scripts/arbol.py`. **No lo edites a mano**: se reescribe cada vez.",
        f"> Árbol visual: `{SALIDA_ALUMNOS}/{alumno['nombre']}.html` (navegador) · [[{alumno['nombre']}.canvas]] (Obsidian)",
        "", "## Resumen", "", "| Nivel | Dominado | % |", "|---|---|---|",
    ]
    for f in calc["por_nivel"]:
        barra = "█" * (f["pct"] // 10) + "░" * (10 - f["pct"] // 10)
        lineas.append(f"| {f['nivel']} | {f['dominados']}/{f['total']} | {barra} {f['pct']} % |")
    lineas += ["", "## ▶️ Siguiente paso recomendado"]
    lineas += [f"{i}. {enl(s['id'])} — {s['motivo']}" for i, s in enumerate(calc["siguiente"], 1)] or ["- (nada disponible)"]
    if calc["meta"]:
        lineas += ["", f"## 🎯 Ruta hacia la meta: {meta_txt} ({len(calc['ruta'])} pasos)"]
        lineas += [f"{i}. {ICONO[est[n]]} {enl(n)}" for i, n in enumerate(calc["ruta"], 1)] or ["- ¡Meta conseguida! 🎉"]
    for titulo, filtro in (("🟡 En curso", "en_curso"), ("🔓 Disponible ahora", "disponible")):
        lineas += ["", f"## {titulo}"]
        lineas += [f"- {enl(n)}" for n in sorted(nodos, key=lambda k: nodos[k]["codigo"]) if est[n] == filtro] or ["- —"]
    lineas += ["", "## 🔒 Próximos desbloqueos (y qué falta)"]
    proximos = [n for n in sorted(nodos, key=lambda k: nodos[k]["codigo"]) if est[n] == "proximo"]
    lineas += [f"- {enl(n)} — falta: {', '.join(enl(f) for f in calc['faltan'][n])}" for n in proximos] or ["- —"]
    lineas += ["", "## ✅ Ya puede hacer (situaciones dominadas)"]
    lineas += [f"- {enl(n)}" for n in sorted(situaciones_dom, key=lambda k: nodos[k]["codigo"])] or ["- —"]
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")


def escribir_panel(ruta, alumnos, calculos, nodos, hoy):
    orden_estado = {"activo": 0, "prueba": 1, "pausa": 2, "antiguo": 3}
    lineas = [
        "---", "tipo: sistema", "---", "# 📊 Panel de progreso", "",
        f"> Generado por `arbol.py` el {hoy.isoformat()}. No editar a mano.", "",
        "## Alumnos", "",
        "| Alumno | Estado | Nivel completado | En curso | Progreso | Logrados 30 días | Sesiones | Última | Siguiente paso | Pasos a la meta |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for nombre in sorted(alumnos, key=lambda k: (orden_estado.get(alumnos[k]["props"].get("estado"), 9), k)):
        a, c = alumnos[nombre], calculos[nombre]
        sig = f"[[{c['siguiente'][0]['id']}]]" if c["siguiente"] else "—"
        lineas.append(f"| [[{nombre} - Ruta\\|{nombre}]] | {a['props'].get('estado', '')} | {c['completado'] or '—'} | "
                      f"{c['trabajando']} | {c['progreso']} % | {c['recientes']} | {a['sesiones']} | {a['ultima'] or '—'} | "
                      f"{sig} | {len(c['ruta']) if c['meta'] else '—'} |")
    lineas += ["", "## 🧱 Cuellos de botella (para optimizar materiales)", "",
               "Nodos que más sesiones necesitan de media hasta lograrse. Si un nodo está aquí, mejora su material o divídelo.", "",
               "| Nodo | Sesiones de media | Alumnos que lo lograron |", "|---|---|---|"]
    medias = {k: v for k, v in sesiones_hasta_dominar(alumnos).items() if v[0] > 1}
    for nid, (media, n) in sorted(medias.items(), key=lambda kv: (-kv[1][0], kv[0]))[:10]:
        lineas.append(f"| [[{nid}]] | {media:.1f} | {n} |")
    if not medias:
        lineas.append("| — | — | — |")
    atascados = {}
    for c in calculos.values():
        for nid, e in c["estado"].items():
            if e == "en_curso":
                atascados[nid] = atascados.get(nid, 0) + 1
    lineas += ["", "## 🟡 Nodos en curso ahora (cuántos alumnos)", ""]
    lineas += [f"- [[{nid}]] — {k}" for nid, k in sorted(atascados.items(), key=lambda kv: -kv[1])] or ["- —"]
    sin_material = [n for n in nodos.values() if n["rama"] == "situacion" and not n["materiales"]]
    lineas += ["", f"## 📦 Situaciones sin material: {len(sin_material)} de "
               f"{sum(1 for n in nodos.values() if n['rama'] == 'situacion')}", "",
               "Prioriza crear material para las situaciones que tus alumnos tienen *disponibles* o *en curso*."]
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- main

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--boveda", default=str(Path(__file__).resolve().parents[2]), help="Raíz de la bóveda")
    parser.add_argument("--validar", action="store_true", help="Solo revisar el árbol")
    parser.add_argument("--alumno", help="Generar solo este alumno (nombre de su ficha)")
    parser.add_argument("--hoy", help="Fecha de referencia AAAA-MM-DD (por defecto, hoy)")
    args = parser.parse_args()

    raiz = Path(args.boveda)
    hoy = date.fromisoformat(args.hoy) if args.hoy else date.today()
    nodos, resolver, avisos, errores = cargar_arbol(raiz)
    print(f"Árbol: {len(nodos)} nodos, {sum(len(n['requiere']) for n in nodos.values())} conexiones")
    if args.validar:
        for e in errores:
            print("❌", e)
        for a in avisos:
            print("⚠️ ", a)
        print("Todo correcto ✅" if not errores and not avisos else f"{len(errores)} errores, {len(avisos)} avisos")
        return 1 if errores else 0
    if errores:
        for e in errores:
            print("❌", e)
        print("Corrige los errores (o ejecuta con --validar para ver el detalle).")
        return 1

    pos, bandas, carriles, ancho, alto = disponer(nodos)
    datos = datos_html(nodos, pos, bandas, carriles, ancho, alto)
    escribir_html(raiz / f"{MAESTRO}.html", "Árbol de habilidades A0–B2",
                  "Mapa completo: situaciones, gramática y vocabulario, y qué desbloquea qué.", dict(datos, modo="maestro"))
    escribir_canvas(raiz / f"{MAESTRO}.canvas", nodos, pos, bandas)
    print(f"✔ {MAESTRO}.html / .canvas")

    alumnos = cargar_alumnos(raiz, resolver, avisos)
    calculos = {}
    for nombre, a in alumnos.items():
        calc = calcular(a, nodos, resolver, hoy)
        calculos[nombre] = calc
        if args.alumno and nombre != args.alumno:
            continue
        salida = raiz / SALIDA_ALUMNOS
        sub = (f"Nivel completado: {calc['completado'] or '—'} · En curso: {calc['trabajando']} "
               f"({calc['progreso']} %) · Actualizado {hoy.isoformat()}")
        d = datos_html(nodos, pos, bandas, carriles, ancho, alto, calc)
        d.update(modo="alumno", por_nivel=calc["por_nivel"], siguiente=calc["siguiente"], meta=calc["meta"],
                 resumen={"completado": calc["completado"], "trabajando": calc["trabajando"],
                          "progreso": calc["progreso"], "recientes": calc["recientes"],
                          "sesiones": a["sesiones"], "ultima": a["ultima"], "pasos": len(calc["ruta"])})
        escribir_html(salida / f"{nombre}.html", f"Árbol de {nombre}", sub, d)
        escribir_canvas(salida / f"{nombre}.canvas", nodos, pos, bandas, calc)
        escribir_ruta_md(salida / f"{nombre} - Ruta.md", a, nodos, calc, hoy)
        print(f"✔ {nombre}: {calc['completado'] or '—'} completado, en curso {calc['trabajando']} {calc['progreso']} %")
    if alumnos and not args.alumno:
        escribir_panel(raiz / SALIDA_ALUMNOS / "Panel de progreso.md", alumnos, calculos, nodos, hoy)
        print(f"✔ {SALIDA_ALUMNOS}/Panel de progreso.md")
    for a in avisos:
        print("⚠️ ", a)
    return 0


PLANTILLA_HTML = r"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITULO__</title>
<style>
:root{--bg:#f8fafc;--panel:#fff;--text:#0f172a;--muted:#64748b;--line:#94a3b8;--band:#f1f5f9;--border:#e2e8f0;
--dom-bg:#dcfce7;--dom-bd:#16a34a;--cur-bg:#fef3c7;--cur-bd:#d97706;--dis-bg:#fff;--dis-bd:#2563eb;
--pro-bg:#f1f5f9;--pro-bd:#94a3b8;--blo-bg:#f8fafc;--blo-bd:#e2e8f0;--sit:#f97316;--gra:#8b5cf6;--voc:#14b8a6;
--accent:#2563eb;--route:#e11d48}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0b1120;--panel:#111827;--text:#e5e7eb;--muted:#94a3b8;
--line:#64748b;--band:#0f172a;--border:#1f2937;--dom-bg:#14532d;--dom-bd:#22c55e;--cur-bg:#713f12;--cur-bd:#f59e0b;
--dis-bg:#111827;--dis-bd:#60a5fa;--pro-bg:#1f2937;--pro-bd:#64748b;--blo-bg:#0f172a;--blo-bd:#1e293b;--accent:#60a5fa;--route:#fb7185}}
:root[data-theme="dark"]{--bg:#0b1120;--panel:#111827;--text:#e5e7eb;--muted:#94a3b8;--line:#64748b;--band:#0f172a;
--border:#1f2937;--dom-bg:#14532d;--dom-bd:#22c55e;--cur-bg:#713f12;--cur-bd:#f59e0b;--dis-bg:#111827;--dis-bd:#60a5fa;
--pro-bg:#1f2937;--pro-bd:#64748b;--blo-bg:#0f172a;--blo-bd:#1e293b;--accent:#60a5fa;--route:#fb7185}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font:14px/1.45 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
header{padding:20px 16px 4px;max-width:1520px;margin:0 auto}
h1{font-size:22px;margin:0 0 4px}
.sub{color:var(--muted);margin:0 0 12px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px}
.chip{background:var(--panel);border:1px solid var(--border);border-radius:999px;padding:4px 12px}
.chip b{font-variant-numeric:tabular-nums}
.levels{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:8px;margin-bottom:12px}
.lvl{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:8px 10px;font-variant-numeric:tabular-nums}
.bar{height:6px;background:var(--band);border-radius:3px;overflow:hidden;margin-top:6px}
.bar i{display:block;height:100%;background:var(--dom-bd)}
.toolbar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:4px 0 8px}
button.t{border:1px solid var(--border);background:var(--panel);color:var(--text);border-radius:8px;padding:6px 10px;cursor:pointer;font:inherit}
button.t[aria-pressed="true"]{border-color:var(--accent);box-shadow:inset 0 0 0 1px var(--accent)}
.legend{display:flex;flex-wrap:wrap;gap:14px;color:var(--muted);font-size:13px;margin-bottom:10px}
.sw{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:5px;vertical-align:-2px;border:2px solid}
main{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:12px;max-width:1520px;margin:0 auto;padding:0 16px 24px}
@media (max-width:900px){main{grid-template-columns:minmax(0,1fr)}}
.tree{overflow:auto;background:var(--panel);border:1px solid var(--border);border-radius:12px;max-height:80vh}
aside{background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:14px 16px;align-self:start;position:sticky;top:12px;max-height:80vh;overflow:auto}
aside h2{font-size:16px;margin:0 0 6px}
aside h3{font-size:13px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);margin:14px 0 6px}
aside ul,aside ol{margin:0;padding-left:18px}
aside li{margin:3px 0}
.link{color:var(--accent);cursor:pointer;text-decoration:underline;text-underline-offset:2px}
.muted{color:var(--muted)}
.mision{background:var(--band);border-radius:8px;padding:8px 10px;margin:8px 0}
.tag{display:inline-block;border-radius:6px;padding:1px 8px;font-size:12px;border:1px solid var(--border);margin-right:4px}
svg .n{cursor:pointer}
svg .n:focus{outline:none}
svg .n:focus rect.box{stroke:var(--accent);stroke-width:3}
svg text{fill:var(--text)}
svg .cod{fill:var(--muted);font-size:11px}
svg .tit{font-size:12.5px}
svg .banda{fill:var(--band)}
svg .bandlbl{font-size:15px;font-weight:700}
svg .carril{fill:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.05em}
svg path.e{fill:none;stroke:var(--line);stroke-width:1.2;opacity:.35}
svg path.e.hl{stroke:var(--accent);opacity:1;stroke-width:2}
svg path.e.rt{stroke:var(--route);opacity:.9;stroke-width:2}
</style>
</head>
<body>
<header>
  <h1 id="titulo"></h1>
  <p class="sub" id="subtitulo"></p>
  <div class="chips" id="chips"></div>
  <div class="levels" id="niveles"></div>
  <div class="toolbar" id="toolbar"></div>
  <div class="legend" id="leyenda"></div>
</header>
<main>
  <div class="tree" id="arbol"></div>
  <aside id="panel" aria-live="polite"></aside>
</main>
<script>
const D = __DATOS__;
const ALUMNO = D.modo === "alumno";
const byId = Object.fromEntries(D.nodos.map(n => [n.id, n]));
const hijos = {};
D.nodos.forEach(n => n.requiere.forEach(r => (hijos[r] = hijos[r] || []).push(n.id)));
const RAMA = {situacion: ["var(--sit)", "Situación"], gramatica: ["var(--gra)", "Gramática"], vocabulario: ["var(--voc)", "Vocabulario"]};
const EST = {
  dominado: ["Dominado", "✓", "dom"], en_curso: ["En curso", "●", "cur"], disponible: ["Disponible", "○", "dis"],
  proximo: ["Próximo (aún bloqueado)", "🔒", "pro"], bloqueado: ["Bloqueado", "🔒", "blo"]
};
const VISIBLES = new Set(["dominado", "en_curso", "disponible", "proximo"]);
let verTodo = !ALUMNO, verRuta = false, filtroRama = "", sel = null;
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
const visible = n => !ALUMNO || verTodo || VISIBLES.has(n.estado) || (verRuta && (n.en_ruta || n.id === D.meta));

function partir(t, max) {
  const out = []; let l = "";
  for (const w of t.split(" ")) {
    if ((l + " " + w).trim().length > max) { out.push(l.trim()); l = w; } else l += " " + w;
  }
  out.push(l.trim());
  if (out.length > 2) { out.length = 2; out[1] = out[1].replace(/.{0,2}$/, "…"); }
  return out;
}

function cabecera() {
  document.getElementById("titulo").textContent = D.titulo;
  document.getElementById("subtitulo").textContent = D.subtitulo;
  const chips = [];
  if (ALUMNO) {
    const r = D.resumen;
    chips.push(["Nivel completado", r.completado || "—"], ["En curso", `${r.trabajando} · ${r.progreso} %`],
      ["Logrados (30 días)", r.recientes], ["Sesiones", r.sesiones]);
    if (D.meta) chips.push(["Meta", `${byId[D.meta].codigo} · ${r.pasos} pasos`]);
  } else {
    for (const k of ["situacion", "gramatica", "vocabulario"])
      chips.push([RAMA[k][1], D.nodos.filter(n => n.rama === k).length]);
    chips.push(["Conexiones", D.nodos.reduce((s, n) => s + n.requiere.length, 0)]);
  }
  document.getElementById("chips").innerHTML = chips.map(([k, v]) => `<span class="chip">${esc(k)}: <b>${esc(v)}</b></span>`).join("");
  const niv = ALUMNO ? D.por_nivel : D.bandas.map(b => ({nivel: b.nivel, total: D.nodos.filter(n => n.nivel === b.nivel).length}));
  document.getElementById("niveles").innerHTML = niv.map(f => ALUMNO
    ? `<div class="lvl"><b>${f.nivel}</b> · ${f.dominados}/${f.total} <span class="muted">(${f.pct} %)</span><div class="bar"><i style="width:${f.pct}%"></i></div></div>`
    : `<div class="lvl"><b>${f.nivel}</b> · ${f.total} nodos</div>`).join("");
  const tb = [];
  if (ALUMNO) tb.push(`<button class="t" id="bTodo" aria-pressed="false">Ver todo (vista profe)</button>`);
  if (ALUMNO && D.meta) tb.push(`<button class="t" id="bRuta" aria-pressed="false">Resaltar ruta a la meta</button>`);
  tb.push(...[["", "Todas"], ["situacion", "Situaciones"], ["gramatica", "Gramática"], ["vocabulario", "Vocabulario"]]
    .map(([k, l]) => `<button class="t rama" data-r="${k}" aria-pressed="${k === filtroRama}">${l}</button>`));
  document.getElementById("toolbar").innerHTML = tb.join("");
  const ley = Object.entries(RAMA).map(([, [c, l]]) => `<span><span class="sw" style="background:${c};border-color:${c}"></span>${l}</span>`);
  if (ALUMNO) for (const k of ["dominado", "en_curso", "disponible", "proximo"])
    ley.push(`<span><span class="sw" style="background:var(--${EST[k][2]}-bg);border-color:var(--${EST[k][2]}-bd)"></span>${EST[k][1]} ${EST[k][0]}</span>`);
  document.getElementById("leyenda").innerHTML = ley.join("");
  const bt = document.getElementById("bTodo");
  if (bt) bt.onclick = () => { verTodo = !verTodo; bt.setAttribute("aria-pressed", verTodo); dibujar(); };
  const br = document.getElementById("bRuta");
  if (br) br.onclick = () => { verRuta = !verRuta; br.setAttribute("aria-pressed", verRuta); dibujar(); panel(); };
  document.querySelectorAll("button.rama").forEach(b => b.onclick = () => {
    filtroRama = b.dataset.r;
    document.querySelectorAll("button.rama").forEach(x => x.setAttribute("aria-pressed", x === b));
    dibujar();
  });
}

function dibujar() {
  const {W, H} = D, s = [];
  s.push(`<svg xmlns="http://www.w3.org/2000/svg" width="${D.ancho}" height="${D.alto}" role="img" aria-label="${esc(D.titulo)}">`);
  for (const b of D.bandas) {
    s.push(`<rect class="banda" x="8" y="${b.y}" width="${D.ancho - 16}" height="${b.h}" rx="12"/>`);
    s.push(`<text class="bandlbl" x="22" y="${b.y + 24}">${b.nivel}</text>`);
    for (const c of D.carriles) s.push(`<text class="carril" x="${c.x + 46}" y="${b.y + 24}">${c.nombre}</text>`);
  }
  const relac = new Set();
  if (sel) { relac.add(sel); byId[sel].requiere.forEach(r => relac.add(r)); (hijos[sel] || []).forEach(h => relac.add(h)); }
  for (const n of D.nodos) {
    if (!visible(n)) continue;
    for (const r of n.requiere) {
      const p = byId[r];
      if (!p || !visible(p)) continue;
      let d;
      if (n.y > p.y + H / 2) {
        const x1 = p.x + W / 2, y1 = p.y + H, x2 = n.x + W / 2, y2 = n.y, dy = Math.max(24, (y2 - y1) / 2);
        d = `M${x1} ${y1} C${x1} ${y1 + dy},${x2} ${y2 - dy},${x2} ${y2}`;
      } else {
        const izq = p.x < n.x, x1 = izq ? p.x + W : p.x, y1 = p.y + H / 2, x2 = izq ? n.x : n.x + W, y2 = n.y + H / 2, dx = izq ? 30 : -30;
        d = `M${x1} ${y1} C${x1 + dx} ${y1},${x2 - dx} ${y2},${x2} ${y2}`;
      }
      const hl = sel && (n.id === sel || r === sel), rt = verRuta && n.en_ruta && (p.en_ruta || p.estado === "dominado");
      s.push(`<path class="e${hl ? " hl" : rt ? " rt" : ""}" d="${d}"/>`);
    }
  }
  for (const n of D.nodos) {
    if (!visible(n)) continue;
    const e = ALUMNO ? EST[n.estado] : null;
    const bg = e ? `var(--${e[2]}-bg)` : "var(--panel)", bd = e ? `var(--${e[2]}-bd)` : "var(--border)";
    let op = 1;
    if (filtroRama && n.rama !== filtroRama) op = .2;
    if (sel && !relac.has(n.id)) op = Math.min(op, .35);
    if (ALUMNO && n.estado === "bloqueado") op = Math.min(op, .45);
    const ruta = verRuta && n.en_ruta, dash = ALUMNO && (n.estado === "proximo" || n.estado === "bloqueado") ? ` stroke-dasharray="4 3"` : "";
    const lineas = partir(n.titulo, 28);
    s.push(`<g class="n" data-id="${esc(n.id)}" tabindex="0" role="button" aria-label="${esc(n.codigo + " " + n.titulo)}" opacity="${op}" transform="translate(${n.x},${n.y})">`);
    s.push(`<rect class="box" width="${W}" height="${H}" rx="9" fill="${bg}" stroke="${ruta ? "var(--route)" : n.id === sel ? "var(--accent)" : bd}" stroke-width="${ruta || n.id === sel ? 2.5 : 1.5}"${dash}/>`);
    s.push(`<rect x="0" y="0" width="5" height="${H}" rx="2" fill="${RAMA[n.rama] ? RAMA[n.rama][0] : "var(--line)"}"/>`);
    s.push(`<text class="cod" x="13" y="16">${esc(n.codigo)}</text>`);
    if (e) s.push(`<text class="cod" x="${W - 10}" y="16" text-anchor="end">${e[1]}</text>`);
    lineas.forEach((l, i) => s.push(`<text class="tit" x="13" y="${33 + i * 15}">${esc(l)}</text>`));
    s.push(`</g>`);
  }
  s.push(`</svg>`);
  const cont = document.getElementById("arbol");
  cont.innerHTML = s.join("");
  cont.querySelectorAll("g.n").forEach(g => {
    g.onclick = () => seleccionar(g.dataset.id);
    g.onkeydown = ev => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); seleccionar(g.dataset.id); } };
  });
}

function enlace(id, siempre) {
  const n = byId[id]; if (!n) return esc(id);
  const ic = ALUMNO ? EST[n.estado][1] + " " : "";
  if (siempre && !visible(n)) return `${ic}<b>${esc(n.codigo)} ${esc(n.titulo)}</b>`;
  return visible(n) ? `${ic}<span class="link" data-id="${esc(id)}">${esc(n.codigo)} ${esc(n.titulo)}</span>`
                    : `${ic}<span class="muted">${esc(n.codigo)} (oculto)</span>`;
}

function seleccionar(id, desplazar) {
  sel = sel === id && !desplazar ? null : id;
  dibujar(); panel();
  if (sel && desplazar) {
    const g = document.querySelector(`g.n[data-id="${CSS.escape(sel)}"]`);
    if (g) g.scrollIntoView({block: "center", inline: "center", behavior: "smooth"});
  }
}

function panel() {
  const p = document.getElementById("panel"), h = [];
  if (!sel) {
    if (ALUMNO) {
      h.push(`<h2>▶️ Siguiente paso</h2><ol>${D.siguiente.map(x => `<li>${enlace(x.id)}<br><span class="muted">${esc(x.motivo)}</span></li>`).join("") || "<li>—</li>"}</ol>`);
      if (D.meta) {
        const ruta = D.nodos.filter(n => n.en_ruta).length;
        h.push(`<h3>🎯 Meta</h3><p>${enlace(D.meta, true)}<br><span class="muted">${ruta ? ruta + " pasos pendientes. Pulsa «Resaltar ruta a la meta»." : "¡Conseguida! 🎉"}</span></p>`);
      }
      h.push(`<h3>Cómo leer el árbol</h3><p class="muted">Solo ves lo que ya dominas, lo que puedes practicar ahora y lo que se desbloquea justo después. Toca un nodo para ver su misión, sus goals y qué te falta.</p>`);
    } else {
      h.push(`<h2>Árbol completo</h2><p class="muted">Toca un nodo para ver su misión, qué necesita y qué desbloquea. Las flechas van del requisito al nodo que abre.</p>`);
    }
    p.innerHTML = h.join(""); return;
  }
  const n = byId[sel], e = ALUMNO ? EST[n.estado] : null;
  h.push(`<span class="tag">${esc(n.nivel)}</span><span class="tag">${esc(RAMA[n.rama] ? RAMA[n.rama][1] : n.rama)}</span>${e ? `<span class="tag">${e[1]} ${e[0]}</span>` : ""}`);
  h.push(`<h2 style="margin-top:8px">${esc(n.codigo)} ${esc(n.titulo)}</h2>`);
  if (n.logro) h.push(`<p class="muted">Logrado el ${esc(n.logro)}</p>`);
  if (n.mision) h.push(`<div class="mision">🎯 ${esc(n.mision)}</div>`);
  if (n.goals.length) h.push(`<h3>Goals</h3><ul>${n.goals.map(g => `<li>${esc(g)}</li>`).join("")}</ul>`);
  if (ALUMNO && n.faltan && n.faltan.length) h.push(`<h3>Le falta</h3><ul>${n.faltan.map(f => `<li>${enlace(f)}</li>`).join("")}</ul>`);
  h.push(`<h3>Requiere</h3><ul>${n.requiere.map(r => `<li>${enlace(r)}</li>`).join("") || "<li class='muted'>Nada: es un punto de partida</li>"}</ul>`);
  const hs = (hijos[n.id] || []);
  h.push(`<h3>Desbloquea</h3><ul>${hs.map(x => `<li>${enlace(x)}</li>`).join("") || "<li class='muted'>—</li>"}</ul>`);
  const abierto = !ALUMNO || ["dominado", "en_curso", "disponible"].includes(n.estado);
  if (n.materiales.length) h.push(abierto
    ? `<h3>Materiales</h3><ul>${n.materiales.map(m => `<li>${esc(m.titulo)}${m.formato ? ` <span class="muted">(${esc(m.formato)})</span>` : ""}</li>`).join("")}</ul>`
    : `<h3>Materiales</h3><p class="muted">🔒 ${n.materiales.length} material(es) se abrirán al desbloquear este nodo.</p>`);
  h.push(`<p class="muted" style="margin-top:14px">Nota: <code>${esc(n.ruta)}</code></p>`);
  h.push(`<p><span class="link" data-close="1">← Volver</span></p>`);
  p.innerHTML = h.join("");
}

document.getElementById("panel").addEventListener("click", ev => {
  const t = ev.target.closest("[data-id],[data-close]");
  if (!t) return;
  if (t.dataset.close) { sel = null; dibujar(); panel(); } else seleccionar(t.dataset.id, true);
});
cabecera(); dibujar(); panel();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    sys.exit(main())

"""Tests del pipeline. Ejecutar desde la raíz:  python -m pytest 00_Sistema/tests -q

No llaman a ninguna API ni necesitan DaVinci: verifican la lógica que, si falla,
rompe la ingesta o hace pagar dos veces.
"""

from __future__ import annotations

import json
import runpy
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from swa import assets, autocut, edicion, guion, kit, naming  # noqa: E402
from swa.config import RAIZ, cargar_config, cargar_curriculo  # noqa: E402

CFG = cargar_config()
CURRICULO = cargar_curriculo()


# --- nomenclatura -----------------------------------------------------------

def test_nombres_de_leccion():
    lec = naming.Leccion(1, 2, "Algoritmo")
    assert lec.guion == "M01_L02_Algoritmo.md"
    assert lec.archivo("RAW", ".mp4") == "M01_L02_Algoritmo_RAW.mp4"
    assert lec.archivo("FINAL", ".mp4") == "M01_L02_Algoritmo_FINAL.mp4"
    assert lec.asset(7, ".mp4") == "M01_L02_007.mp4"
    assert naming.workbook(3) == "M03_Workbook.pdf"


@pytest.mark.parametrize("nombre,esperado", [
    ("M01_L01_Nicho_RAW", {"modulo": 1, "leccion": 1, "clave": "Nicho", "tipo": "RAW"}),
    ("M12_L03_VideoIntro", {"modulo": 12, "leccion": 3, "clave": "VideoIntro", "tipo": None}),
    ("M1_L01_Nicho_RAW", None),          # módulo sin cero
    ("M01_L01_Nicho_raw", None),         # tipo en minúsculas
    ("M01_L01_Reseñas", None),           # ñ
    ("M01-L01-Nicho", None),
])
def test_analizar_nombres(nombre, esperado):
    assert naming.analizar(nombre) == esperado


def test_curriculo_valido():
    assert naming.validar_curriculo(CURRICULO) == []


def test_curriculo_detecta_errores():
    malo = {"modulos": [{"numero": 1, "lecciones": [
        {"numero": 1, "clave": "Reseñas"}, {"numero": 1, "clave": "Otra"}]}]}
    errores = naming.validar_curriculo(malo)
    assert any("Clave inválida" in e for e in errores)
    assert any("duplicada" in e for e in errores)


# --- parser de guiones ------------------------------------------------------

GUION = """---
leccion: M01_L01
clave: Nicho
---
# Título

## Hook
[BROLL: busy online market]
Uno dos tres cuatro.
<!-- comentario [IMG: no cuenta] -->
[SLIDE: Fórmula | Alumno | Problema]
cinco seis.
[TAREA: Haz esto]
Contenido **del** workbook [IMG: tampoco cuenta]
[/TAREA]
siete.
[ROADMAP]
[PANTALLA: abre Preply]
"""


def test_parser_etiquetas_y_posiciones():
    g = guion.parsear(GUION)
    assert g.errores == []
    assert [e.tipo for e in g.etiquetas] == ["BROLL", "SLIDE", "ROADMAP", "PANTALLA"]
    assert [e.palabra for e in g.etiquetas] == [0, 4, 7, 7]
    assert g.etiquetas[1].partes == ["Fórmula", "Alumno", "Problema"]
    assert g.etiquetas[0].seccion == "Hook"
    assert g.palabras == ["Uno", "dos", "tres", "cuatro", "cinco", "seis", "siete"]
    assert len(g.bloques) == 1 and g.bloques[0].titulo == "Haz esto"
    assert "Contenido **del** workbook" in g.bloques[0].contenido


@pytest.mark.parametrize("texto,error", [
    ("[TAREA: x]\nsin cierre", "sin cierre"),
    ("hola [/RECURSO]", "sin apertura"),
    ("[BROLL]", "necesita descripción"),
    ("[VIDEO: algo]", "desconocida"),
])
def test_parser_errores(texto, error):
    assert any(error in e for e in guion.parsear(texto).errores)


def test_guion_de_ejemplo_es_valido():
    lec = naming.buscar_leccion(CURRICULO, 1, 1)
    g = guion.validar(guion.cargar(CFG.ruta("guiones") / lec.guion), lec)
    assert g.errores == []
    assert g.de_tipo("ROADMAP")


# --- auto-cut ---------------------------------------------------------------

STDERR = """
[silencedetect @ 0x1] silence_start: 3.0
[silencedetect @ 0x1] silence_end: 5.0 | silence_duration: 2.0
[silencedetect @ 0x1] silence_start: 8.0
[silencedetect @ 0x1] silence_end: 8.1 | silence_duration: 0.1
[silencedetect @ 0x1] silence_start: 8.2
[silencedetect @ 0x1] silence_end: 10.5 | silence_duration: 2.3
[silencedetect @ 0x1] silence_start: 11.8
"""


def test_parsear_silencedetect_con_silencio_final():
    s = autocut.parsear_silencedetect(STDERR, 12.0)
    assert s == [(3.0, 5.0), (8.0, 8.1), (8.2, 10.5), (11.8, 12.0)]


def test_segmentos_con_voz_margen_y_clics():
    s = autocut.parsear_silencedetect(STDERR, 12.0)
    seg = autocut.segmentos_con_voz(s, 12.0, margen=0.15, minimo_segmento=0.3)
    # 8.1-8.2 es un clic de 0.1 s: se descarta
    assert seg == [(0.0, 3.15), (4.85, 8.15), (10.35, 11.95)]
    assert autocut.duracion_total(seg) == pytest.approx(3.15 + 3.3 + 1.6)


def test_segmentos_se_unen_si_el_margen_solapa():
    seg = autocut.segmentos_con_voz([(2.0, 2.2)], 5.0, margen=0.15, minimo_segmento=0.3)
    assert seg == [(0.0, 5.0)]


@pytest.mark.parametrize("t,esperado", [(1.0, 1.0), (4.0, 3.0), (6.0, 4.0), (9.0, 6.0), (20.0, 6.0)])
def test_raw_a_final(t, esperado):
    assert autocut.raw_a_final(t, [(0.0, 3.0), (5.0, 8.0)]) == pytest.approx(esperado)


# --- sincronización ---------------------------------------------------------

def test_alinear_tolera_improvisacion():
    guion_palabras = "Hola soy Alfy y hoy vamos a elegir tu nicho".split()
    audio = [{"word": w, "start": i * 1.0, "end": i * 1.0 + 0.5} for i, w in
             enumerate("hola eh soy alfy y hoy hoy vamos a elegir tu nicho".split())]
    mapa = edicion.alinear(guion_palabras, audio)
    assert mapa[0] == 0.5            # "Hola"
    assert mapa[9] == 11.5           # "nicho" (última palabra)
    # etiqueta antes de "vamos" (índice 5) -> fin del "hoy" alineado (dicho dos veces)
    assert edicion.tiempo_etiqueta(5, mapa) in (5.5, 6.5)
    assert edicion.tiempo_etiqueta(6, mapa) == 7.5  # justo después de "vamos"


def test_normalizar_quita_tildes_y_puntuacion():
    assert edicion.normalizar("¡Módulo!") == "modulo"


# --- assets y caché ---------------------------------------------------------

def _plan_ejemplo():
    lec = naming.buscar_leccion(CURRICULO, 1, 1)
    g = guion.cargar(CFG.ruta("guiones") / lec.guion)
    return lec, assets.planificar(g, lec, CFG, CURRICULO)


def test_plan_de_assets_nombres_y_proveedores():
    lec, plan = _plan_ejemplo()
    por_tipo = {}
    for i in plan:
        por_tipo.setdefault(i.tipo, []).append(i)
    assert [i.destino.name for i in por_tipo["BROLL"]] == ["M01_L01_001.mp4", "M01_L01_002.mp4"]
    assert por_tipo["ROADMAP"][0].destino.name == "M01_Roadmap.png"
    assert all(i.es_local for i in por_tipo["SLIDE"])
    assert por_tipo["BROLL"][0].proveedor == CFG["proveedores"]["video"]
    assert CFG["estilo_visual"]["video"] in por_tipo["BROLL"][0].prompt


def test_cache_no_paga_dos_veces():
    _, plan = _plan_ejemplo()
    item = next(i for i in plan if i.tipo == "BROLL")
    # Simula que el mismo prompt ya se pagó y se guardó con otro nombre
    otro = RAIZ / "03_Assets_Generados" / "_test_pagado.mp4"
    otro.write_bytes(b"x")
    try:
        manifest = {item.huella: {"archivo": "03_Assets_Generados/_test_pagado.mp4"}}
        assert assets.estado_item(item, manifest) == "copiar"
        assert assets.estado_item(item, {}) == "generar"
    finally:
        otro.unlink()


def test_huella_cambia_con_el_prompt():
    assert assets.huella("video", "a") != assets.huella("video", "b")
    assert assets.huella("video", "a") == assets.huella("video", "a")


def test_presupuesto_bloquea(monkeypatch):
    lec, _ = _plan_ejemplo()
    datos = dict(CFG.datos, costos_usd={"video": 10.0, "imagen": 1.0, "tts": 1.0},
                 presupuesto_max_usd_por_ejecucion=5.0)
    cfg = type(CFG)(datos)
    plan = assets.planificar(guion.cargar(CFG.ruta("guiones") / lec.guion), lec, cfg, CURRICULO)
    monkeypatch.setattr(assets, "cargar_manifest", lambda _c: {})
    with pytest.raises(RuntimeError, match="supera el tope"):
        assets.generar([i for i in plan if not i.es_local], cfg, dry_run=True, informar=lambda _: None)


# --- kit de grabación -------------------------------------------------------

def test_teleprompter_oculta_bloques_y_muestra_avisos():
    g = guion.parsear(GUION)
    html = kit.cuerpo_teleprompter(g)
    assert "Contenido" not in html                 # el bloque TAREA no se lee
    assert "Tarea: Haz esto (en el workbook)" in html
    assert "cue-pantalla" in html and "abre Preply" in html
    assert "[BROLL" not in html


# --- script de DaVinci con un Resolve simulado -------------------------------

class _Item:
    def __init__(self, ruta, fps="30", frames="150"):
        self.props = {"File Path": ruta, "FPS": fps, "Frames": frames}
        self.set = {}

    def GetClipProperty(self, k):
        return self.props.get(k)

    def GetStart(self):
        return self.start

    def SetProperty(self, k, v):
        self.set[k] = v
        return True


class _Timeline:
    def __init__(self, nombre):
        self.nombre, self.pistas, self.items, self.marcadores = nombre, {"video": 1, "audio": 1}, [], []

    def GetName(self): return self.nombre
    def GetTrackCount(self, t): return self.pistas[t]
    def AddTrack(self, t, *_): self.pistas[t] += 1; return True
    def GetStartFrame(self): return 108000
    def GetItemListInTrack(self, t, i): return [x for x in self.items if x.get("trackIndex", 1) == i]
    def AddMarker(self, *a): self.marcadores.append(a); return True


class _MediaPool:
    def __init__(self):
        self.clips, self.timeline, self.cursor = [], None, 0

    def GetRootFolder(self): return self
    def SetCurrentFolder(self, _): return True
    def GetClipList(self): return self.clips
    def ImportMedia(self, rutas):
        nuevos = [_Item(r) for r in rutas]
        self.clips += nuevos
        return nuevos
    def CreateEmptyTimeline(self, n):
        self.timeline = _Timeline(n)
        return self.timeline
    def AppendToTimeline(self, infos):
        for info in infos:
            obj = _Item("tl")
            obj.__dict__.update(info)
            obj.get = info.get
            if "recordFrame" in info:
                obj.start = info["recordFrame"]
            else:  # append secuencial al final de V1
                obj.start = 108000 + self.cursor
                self.cursor += info["endFrame"] - info["startFrame"] + 1
            self.timeline.items.append(obj)
        return infos


class _Proyecto:
    def __init__(self):
        self.mp, self.ajustes, self.timelines = _MediaPool(), {}, []

    def GetTimelineCount(self): return len(self.timelines)
    def GetTimelineByIndex(self, i): return self.timelines[i - 1]
    def SetSetting(self, k, v): self.ajustes[k] = v; return True
    def GetSetting(self, k): return self.ajustes.get(k)
    def GetMediaPool(self): return self.mp
    def SetCurrentTimeline(self, t): self.timelines.append(t); return True


class _PM:
    def __init__(self): self.p = _Proyecto()
    def LoadProject(self, _): return None
    def CreateProject(self, _): return self.p


class _Resolve:
    def __init__(self): self.pm = _PM()
    def GetProjectManager(self): return self.pm


def test_script_davinci_monta_con_resolve_simulado(tmp_path, monkeypatch):
    plan = {
        "proyecto": "SWA_M01_L01_Nicho", "base": "M01_L01_Nicho", "raw": str(tmp_path / "raw.mp4"),
        "fps": 30.0, "duracion_raw_s": 12.0, "duracion_final_s": 8.1,
        "segmentos": [[0.0, 3.15], [4.85, 8.15], [10.35, 12.0]], "metodo_sincronizacion": "estimacion",
        "secuencia": [
            {"tipo": "raw", "inicio_s": 0.0, "fin_s": 3.15},
            {"tipo": "pausa", "duracion_s": 2.0, "imagen": str(tmp_path / "e.png"), "audio": str(tmp_path / "a.mp3")},
            {"tipo": "raw", "inicio_s": 4.85, "fin_s": 8.15},
            {"tipo": "raw", "inicio_s": 10.35, "fin_s": 12.0},
        ],
        "zoom_punch_in": 1.15,
        "inserciones": [
            {"tipo": "SLIDE", "archivo": str(tmp_path / "s.png"), "pista": "V2", "inicio_s": 1.0, "duracion_s": 5},
            {"tipo": "BROLL", "archivo": str(tmp_path / "b.mp4"), "pista": "V2", "inicio_s": 2.0, "duracion_s": None},
        ],
        "marcadores": [{"inicio_s": 6.0, "color": "Blue", "nombre": "PANTALLA", "nota": "abre Preply"}],
    }
    ruta_plan = tmp_path / "plan.json"
    ruta_plan.write_text(json.dumps(plan))
    resolve_dir = SCRIPTS / "resolve"
    sys.path.insert(0, str(resolve_dir))
    import swa_comun
    monkeypatch.setattr(swa_comun, "cargar_plan", lambda: json.loads(ruta_plan.read_text()))
    falso = _Resolve()
    runpy.run_path(str(resolve_dir / "swa_montar.py"), init_globals={"resolve": falso})

    proyecto = falso.pm.p
    tl = proyecto.mp.timeline
    assert proyecto.ajustes["timelineFrameRate"] == "30"
    v1 = [x for x in tl.items if "trackIndex" not in x.__dict__]
    # tramo · tarjeta Escucha (2 s = 60 frames) · tramo · tramo
    assert [(x.startFrame, x.endFrame) for x in v1] == [(0, 94), (0, 59), (146, 244), (310, 360)]
    assert v1[1].start == 108095
    v2 = [x for x in tl.items if x.__dict__.get("trackIndex") == 2 and x.mediaType == 1]
    # el B-Roll pedido en 2 s se desplaza al final de la slide (1 s + 5 s) para no solaparse
    assert [x.recordFrame - 108000 for x in v2] == [30, 180]
    a2 = [x for x in tl.items if x.__dict__.get("mediaType") == 2]
    assert a2[0].recordFrame == 108095  # el audio suena sobre su tarjeta, no sobre tu voz
    assert tl.pistas == {"video": 2, "audio": 2}
    assert tl.marcadores[0][:3] == (180, "Blue", "PANTALLA")
    zooms = [x.set.get("ZoomX") for x in v1]
    assert zooms == [None, None, 1.15, None]  # punch-in alterno solo en tramos de voz


# --- cliente Apimart con HTTP simulado ----------------------------------------

def test_apimart_sondea_tarea_asincrona(monkeypatch):
    from swa.providers import apimart as mod

    class Resp:
        def __init__(self, datos=None, contenido=b""):
            self.datos, self.content = datos, contenido
        def json(self):
            return self.datos

    respuestas = iter([
        Resp({"code": 200, "data": [{"task_id": "t-1", "status": "submitted"}]}),
        Resp({"data": {"status": "processing"}}),
        Resp({"data": {"status": "completed", "result": {"videos": [{"url": ["https://cdn.x/v.mp4"]}]}}}),
        Resp(contenido=b"MP4"),
    ])
    llamadas = []

    def falsa(metodo, url, **kw):
        llamadas.append((metodo, url))
        return next(respuestas)

    monkeypatch.setattr(mod, "peticion", falsa)
    monkeypatch.setattr(mod, "secreto", lambda _n: "k")
    monkeypatch.setattr(mod.time, "sleep", lambda _s: None)
    cliente = mod.Apimart(dict(CFG["apimart"]))
    assert cliente.video("test") == b"MP4"
    assert llamadas[1] == ("GET", "https://api.apimart.ai/v1/tasks/t-1")
    assert llamadas[-1] == ("GET", "https://cdn.x/v.mp4")


# --- voces, pausas de audio, escenas y materiales ----------------------------

def test_separar_voz_por_papel():
    assert assets.separar_voz("estudiante_us | How long?", CFG) == ("estudiante_us", "How long?")
    assert assets.separar_voz("Specific beats generic.", CFG) == (None, "Specific beats generic.")


def test_validar_voces_detecta_papel_inexistente():
    g = guion.parsear("Hola. [AUDIO: profesor_fr | Bonjour]")
    assert any("profesor_fr" in e for e in assets.validar_voces(g, CFG))
    assert assets.validar_voces(guion.parsear("Hola. [AUDIO: modelo_en | Hi]"), CFG) == []


def test_audio_con_voz_cambia_la_huella():
    lec = naming.Leccion(7, 4, "Listening")
    a = assets.planificar(guion.parsear("Uno. [AUDIO: estudiante_us | Hi]"), lec, CFG, CURRICULO)[0]
    b = assets.planificar(guion.parsear("Uno. [AUDIO: estudiante_uk | Hi]"), lec, CFG, CURRICULO)[0]
    assert (a.voz, a.prompt) == ("estudiante_us", "Hi")
    assert a.huella != b.huella


def test_objetivos_es_local_y_gratis():
    lec = naming.Leccion(1, 1, "Nicho")
    plan = assets.planificar(guion.parsear("Hola. [OBJETIVOS: Uno | Dos]"), lec, CFG, CURRICULO)
    assert plan[0].es_local and plan[0].destino.name == "M01_L01_001.png" and plan[0].coste == 0


def test_intercalar_pausas_parte_el_tramo():
    seg = [(0.0, 4.0), (6.0, 10.0)]   # 8 s de voz
    pausas = [{"en_s": 2.0, "duracion_s": 3.0, "orden": 1}, {"en_s": 8.0, "duracion_s": 1.0, "orden": 5}]
    sec = autocut.intercalar_pausas(seg, pausas)
    assert [(e["tipo"], e.get("inicio_s"), e.get("fin_s")) for e in sec] == [
        ("raw", 0.0, 2.0), ("pausa", None, None), ("raw", 2.0, 4.0), ("raw", 6.0, 10.0), ("pausa", None, None)]


def test_pausa_en_el_limite_va_antes_del_siguiente_tramo():
    sec = autocut.intercalar_pausas([(0.0, 4.0), (6.0, 10.0)], [{"en_s": 4.0, "duracion_s": 1.0, "orden": 0}])
    assert [e["tipo"] for e in sec] == ["raw", "pausa", "raw"]


def test_desplazar_respeta_el_orden_del_guion():
    pausas = [{"en_s": 5.0, "duracion_s": 2.0, "orden": 3}]
    assert autocut.desplazar(4.0, 9, pausas) == 4.0
    assert autocut.desplazar(5.0, 2, pausas) == 5.0   # visual antes del audio en el guion
    assert autocut.desplazar(5.0, 4, pausas) == 7.0   # visual después del audio
    assert autocut.desplazar(6.0, 9, pausas) == 8.0


def test_plan_escenas_vuelve_a_camara_en_el_siguiente_titulo():
    cuerpo = "## Hook\nHola.\n## Demo\n[PANTALLA: abre Preply]\nMira.\n## Cierre\nAdiós."
    texto, cambios = kit.plan_escenas(cuerpo, "Camara", "Clase")
    assert cambios == [("Camara", "inicio"), ("Clase", "Demo"), ("Camara", "Cierre")]
    assert texto.index("[ESCENA: Clase]") < texto.index("[PANTALLA")


def test_materiales_yaml_valido_y_plan():
    from swa import materiales
    datos = materiales.cargar()
    assert materiales.validar(datos, CFG) == []
    plan = materiales.planificar(CFG, CURRICULO, datos, {"MAT01", "AUD01"})
    tipos = [i.tipo for i in plan]
    assert tipos.count("ILUSTRACION") == 1 and tipos.count("MATERIAL") == 1
    assert tipos.count("PISTA") == len(next(m for m in datos["materiales"] if m["id"] == "AUD01")["lineas"])
    assert next(i for i in plan if i.tipo == "MATERIAL").destino.name == "MAT01_MapaMCER.png"


def test_packs_de_audio_reutilizan_la_cache_de_los_guiones():
    """Misma frase y voz en un guion y en materiales.yaml -> misma huella -> no se paga dos veces."""
    from swa import materiales
    pista = next(i for i in materiales.planificar(CFG, CURRICULO, materiales.cargar(), {"AUD02"}) if i.tipo == "PISTA")
    lec = naming.Leccion(7, 1, "Presentacion")
    tag = assets.planificar(guion.parsear(f"Hola. [AUDIO: {pista.voz} | {pista.prompt}]"), lec, CFG, CURRICULO)[0]
    assert tag.huella == pista.huella


def test_materiales_rechaza_ids_y_layouts_invalidos():
    from swa import materiales
    malo = {"materiales": [{"id": "X1", "clave": "Algo", "layout": "lista"},
                           {"id": "MAT02", "clave": "Otro", "layout": "circulo"}]}
    errores = materiales.validar(malo, CFG)
    assert any("X1" in e for e in errores) and any("circulo" in e for e in errores)


def test_roadmap_excluye_modulos_express():
    assert all(m.get("tipo") != "express" for m in naming.modulos_roadmap(CURRICULO))
    assert len(naming.modulos_roadmap(CURRICULO)) < len(CURRICULO["modulos"])

# SpanishWithAlfy Mentoring: fábrica de cursos

Pipeline para producir el curso **"De 0 a Tutor PRO: $1000+ al mes enseñando español online"**, en el que tú solo
**grabas leyendo**. Claude Code escribe los guiones (ya están los 27: 6 módulos + Express de inglés);
Apimart genera B-Roll e ilustraciones; ElevenLabs, las voces; y el resto (materiales entregables,
teleprompter con cambios de escena, Auto-Cut, montaje en DaVinci, render y workbooks PDF) es automático.

```
curriculum.yaml ─► /guion ─► 01_Guiones/M01_L01_Nicho.md
                                   │
            ┌──────────────────────┼─────────────────────────┐
            ▼                      ▼                         ▼
   preparar (assets)        teleprompter + checklist     workbook (PDF)
   Apimart / ElevenLabs /         │
   slides locales                 ▼
            │              🎥 TÚ GRABAS EN OBS ─► 02_Bruto_OBS/..._RAW.mp4
            │                      │
            └──────────► editar (Auto-Cut + sincronización) ─► plan .json
                                   │
                    DaVinci Resolve (gratis): SWA 1 Montar ─► revisar ─► SWA 2 Render
                                   │
                                   ▼
                     05_Renders_Finales/M01_L01_Nicho_FINAL.mp4
```

## Instalación (Windows)

```powershell
git clone <este-repo> C:\SpanishWithAlfy_Mentoring
cd C:\SpanishWithAlfy_Mentoring
winget install Python.Python.3.12
winget install Gyan.FFmpeg
pip install -r requirements.txt
copy .env.example .env        # y pega tus API keys
python -m pytest 00_Sistema/tests -q
python builder.py instalar-davinci
```

Para DaVinci Resolve **gratis**, Resolve necesita un Python 3 instalado en el sistema: el de arriba sirve.
Los scripts aparecen en **Workspace › Scripts**.

## Uso diario

| Momento | Comando | Coste |
|---|---|---|
| Escribir o mejorar un guion | `/guion 01 02` en Claude Code | créditos de Claude |
| Contexto compacto de una lección | `python builder.py contexto 01 02` | $0 |
| Comprobar | `python builder.py validar 01 02` | $0 |
| Ver qué costará | `python builder.py preparar 01 02` | $0 (dry-run) |
| Generar assets | `python builder.py preparar 01 02 --generar` | Apimart/ElevenLabs |
| Grabar | teleprompter `01_Guiones/teleprompter/…html` | tu tiempo |
| Auto-Cut | `python builder.py editar 01 02` | Whisper (opcional, en caché) |
| Montar y render | DaVinci › Workspace › Scripts › SWA 1 / SWA 2 | $0 |
| Materiales entregables y packs de audio | `python builder.py materiales [--generar]` | Apimart/ElevenLabs |
| Materiales web interactivos (HTML) | `python builder.py web [--capturas]` | $0 |
| Workbook | `python builder.py workbook 1` | $0 |
| Ver avance | `python builder.py estado` | $0 |

## Estructura

```
00_Sistema/
  config.yaml           ← proveedores, modelos, marca, presupuesto, umbrales
  curriculum.yaml       ← módulos y lecciones (fuente de verdad)
  materiales.yaml       ← materiales entregables (MCER, plantillas, packs de audio)
  web.yaml              ← materiales web interactivos (calculadora, diagnóstico, cronómetro...)
  scripts/builder.py    ← CLI
  scripts/swa/          ← librería: nomenclatura, parser, assets, autocut, edición, kit, workbook
  scripts/resolve/      ← scripts que corren DENTRO de DaVinci (solo librería estándar)
  templates/            ← guion, teleprompter, workbook, web (swa.css + swa.js), obs
  tests/                ← python -m pytest 00_Sistema/tests -q
01_Guiones/             ← M01_L01_Nicho.md (+ teleprompter/ y checklists)
02_Bruto_OBS/           ← M01_L01_Nicho_RAW.mp4
03_Assets_Generados/    ← BROLL/ IMAGENES/ AUDIO/ SLIDES/ OBJETIVOS/ ROADMAP/ ILUSTRACIONES/ CAPTURAS/ + manifest.json
04_Workbooks/           ← M01_Workbook.pdf + Materiales/ (PNG) + Audios/ (packs) + Web/ (index.html + WEB01…)
05_Renders_Finales/     ← M01_L01_Nicho_FINAL.mp4
.claude/skills/         ← /guion /materiales /produccion /captacion
docs/                   ← formato de guion, guía OBS, proveedores, materiales web, plan y calendario
```

## Protecciones contra gastos
- Todo comando de pago es **dry-run por defecto**; hace falta `--generar`.
- **Caché por contenido**: el mismo prompt con el mismo modelo nunca se paga dos veces.
- **Tope por ejecución** (`presupuesto_max_usd_por_ejecucion`).
- Slides y roadmap se generan **en local a $0**.

Empieza por [`docs/PLAN_DE_PRODUCCION.md`](docs/PLAN_DE_PRODUCCION.md).

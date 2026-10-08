---
name: produccion
description: Prepara una lección para grabar (assets + teleprompter + checklist) o procesa una grabación (Auto-Cut + plan DaVinci).
disable-model-invocation: true
model: haiku
effort: low
argument-hint: "preparar|editar|estado [MM LL]"
---

# /produccion $ARGUMENTS

- `preparar MM LL`: `python builder.py preparar MM LL --breve`. Muestra el coste y pregunta antes de repetir con `--generar`. Después resume en 3 líneas los cambios de escena del checklist (`01_Guiones/teleprompter/*_CHECKLIST.md`).
- `editar MM LL`: comprueba que exista `02_Bruto_OBS/M[MM]_L[LL]_*_RAW.(mp4|mkv|mov)` (si el nombre no es exacto, propón el renombrado). Luego `python builder.py editar MM LL` y di: DaVinci › Workspace › Scripts › SWA 1 - Montar leccion → revisar marcadores (rojo = falta asset) → SWA 2 - Render.
- `estado`: `python builder.py estado` y resume qué falta.
No leas archivos generados (HTML, JSON, PNG): la salida de la CLI basta.

---
name: materiales
description: Crea o mejora materiales entregables (imágenes híbridas Apimart, packs de audio ElevenLabs, workbooks).
disable-model-invocation: true
argument-hint: "[MAT01 AUD02 ... | workbook M]"
---

# /materiales $ARGUMENTS

- Los materiales se definen como DATOS en `00_Sistema/materiales.yaml` (layouts: lista, escalera, linea_tiempo, plantilla, roadmap; `tipo: audio` para packs). Para añadir uno, copia la forma de un material existente: no hace falta código.
- Las ilustraciones se piden en inglés y sin texto; el texto exacto se compone en local.
- Cifras externas (horas MCER, exámenes): `verificado: false` hasta que Alfy las confirme.
- Packs de audio: las mismas frases y voces que los `[AUDIO]` de los guiones (la caché evita pagar dos veces).

Flujo:
1. `python builder.py validar` y después `python builder.py materiales $ARGUMENTS --breve` (dry-run: número de llamadas y coste).
2. Pide confirmación explícita antes de `--generar`.
3. Con `workbook M`: `python builder.py workbook M`.

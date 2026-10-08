---
name: postproduccion
description: Procesa una grabación de OBS ya hecha (Auto-Cut, sincronización de visuales y plan para DaVinci Resolve) y guía el montaje y el render. Úsala cuando Alfy diga "ya grabé M01 L01" o "edita la lección".
---

# Skill: Postproducción

1. Comprueba que existe `02_Bruto_OBS/M[MM]_L[LL]_[Clave]_RAW.mp4` (o .mkv/.mov). Si el nombre no es exacto, propón el renombrado (no renombres sin confirmación).
2. `python builder.py editar MM LL`. La transcripción (Apimart Whisper) cuesta poco y se guarda en caché. Si Alfy no quiere pagarla, usa `--sin-transcripcion`.
3. Informa: duración RAW → final, número de tramos, inserciones, método de sincronización y marcadores `FALTA` (assets sin generar).
4. Indica los pasos en DaVinci Resolve (gratis):
   - Primera vez: `python builder.py instalar-davinci` y reiniciar Resolve.
   - Workspace › Scripts › **SWA 1 - Montar leccion** → revisar marcadores azules (PANTALLA) y rojos (FALTA).
   - Ajustes finos a mano (tomas repetidas, timing de B-Roll).
   - Workspace › Scripts › **SWA 2 - Render** → `05_Renders_Finales/M.._FINAL.mp4`.
5. Si el Auto-Cut corta demasiado o muy poco, ajusta `autocut.umbral_db`, `silencio_min_s` o `margen_s` en `config.yaml` y repite el paso 2. Es gratis porque la transcripción está en caché.

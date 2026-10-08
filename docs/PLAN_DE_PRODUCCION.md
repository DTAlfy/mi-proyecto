# Plan de producción: de cero al lanzamiento

Cada fase tiene un **entregable verificable**. No pases a la siguiente sin cerrar la anterior.

## Fase 0: Puesta a punto (1 tarde)
- [ ] Instalar Python 3.11+, ffmpeg (`winget install Gyan.FFmpeg`), OBS y DaVinci Resolve (gratis)
- [ ] `pip install -r requirements.txt` y `python -m pytest 00_Sistema/tests -q` → todo en verde
- [ ] Copiar `.env.example` a `.env` y pegar las claves de Apimart y ElevenLabs
- [ ] Revisar `docs/PROVEEDORES.md` → verificar rutas/modelos de Apimart y rellenar `costos_usd`
- [ ] `python builder.py comparar-voces "..."` → elegir proveedor de TTS
- [ ] `python builder.py instalar-davinci` y reiniciar Resolve
- [ ] Configurar OBS según `docs/GUIA_GRABACION_OBS.md`
- [ ] Ajustar marca y enlaces en `config.yaml` (colores, Skool, TidyCal, checkout)
- **Entregable:** `python builder.py estado` funciona y los scripts SWA aparecen en Resolve.

## Fase 1: Lección piloto M01_L01 (1-2 días)
Valida el pipeline completo con UNA lección antes de producir en serie.
- [ ] Revisar/ampliar el guion de ejemplo (`/guion 01 01` en Claude Code)
- [ ] `/preparar-grabacion 01 01` → generar assets (primer gasto real, pequeño)
- [ ] Grabar con el teleprompter → `02_Bruto_OBS/M01_L01_Nicho_RAW.mp4`
- [ ] `/postproduccion 01 01` → montar en DaVinci → revisar → render
- [ ] Anotar qué ajustar: umbral del Auto-Cut, estilo visual, duración de slides, zoom
- **Entregable:** `05_Renders_Finales/M01_L01_Nicho_FINAL.mp4` que publicarías tal cual.

## Fase 2: Guiones de todo el curso (Claude Code, créditos de sesión)
- [ ] `/guion 01` ... `/guion 06` (módulo a módulo) → revisar y marcar `estado: revisado`
- [ ] `python builder.py validar` → sin errores
- [ ] `python builder.py preparar MM LL` (dry-run) en cada lección → revisar coste total antes de generar
- **Entregable:** 22 guiones validados y presupuesto de assets conocido.

## Fase 3: Assets en lote
- [ ] `--generar` módulo a módulo (el tope de presupuesto evita sorpresas)
- [ ] Revisar visualmente cada B-Roll; si uno no sirve, cambiar solo su prompt y regenerar (la caché protege el resto)
- **Entregable:** `python builder.py estado` con todos los assets en `N/N`.

## Fase 4: Grabación por bloques
- Graba un módulo por sesión (misma ropa, luz y encuadre). El checklist de cada lección dice qué tener abierto.
- **Entregable:** todos los `_RAW.mp4` con su nombre correcto.

## Fase 5: Postproducción y workbooks
- [ ] `editar` + montar + render de cada lección
- [ ] Capturas de Lightshot/Flameshot en `03_Assets_Generados/CAPTURAS/M[XX]_L[XX]_*.png`
- [ ] `python builder.py workbook 1` ... `6`
- **Entregable:** 22 `_FINAL.mp4` + 6 workbooks PDF.

## Fase 6: Lanzamiento minimalista
- [ ] Skool: aula con los videos y los workbooks; comunidad para dudas entre alumnos
- [ ] Checkout (Gumroad o Stripe): curso self-paced como producto de entrada
- [ ] TidyCal: "Auditoría de Perfil Preply/italki 1 a 1" enlazada desde Skool y desde cada workbook (ya incluida en el PDF)
- [ ] `/captacion`: lead magnet (mini-curso del Módulo 1), página de ventas y Shorts "antes y después" con un único CTA
- **Entregable:** embudo Shorts → lead magnet → curso → mentoría funcionando.

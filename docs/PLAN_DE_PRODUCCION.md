# Plan de producción final

**Estado de partida (ya hecho en el repo):** 27 guiones validados (6 módulos + Express de inglés,
unos 100 min de lectura), 9 materiales entregables, 2 packs de audio, teleprompter y checklist de
cada lección, scripts de DaVinci y workbooks automáticos.

**Presupuesto de APIs del curso completo:** 84 llamadas únicas = 28 B-Roll de video + 25 imágenes
+ 15 ilustraciones (Apimart) + 16 audios (ElevenLabs). Los 17 `[AUDIO]` de los guiones reutilizan las
pistas de los packs: no se pagan dos veces. Rellena `costos_usd` en `config.yaml` y el dry-run te dará la cifra en dólares.

Cada fase termina con un **entregable comprobable**. No pases a la siguiente sin cerrarla.

---

## Fase 0: Puesta a punto del PC (1 tarde)
- [ ] Instalar Python 3.12, ffmpeg (`winget install Gyan.FFmpeg`), OBS y DaVinci Resolve (gratis)
- [ ] Clonar el repo en `C:\SpanishWithAlfy_Mentoring` · `pip install -r requirements.txt`
- [ ] `python -m pytest 00_Sistema/tests -q` → todo en verde
- [ ] `python builder.py instalar-davinci` y reiniciar Resolve → aparecen los scripts SWA
- **Entregable:** `python builder.py estado` muestra 27 guiones ✓.

## Fase 1: Escenas de OBS (45 min)
- [ ] Seguir `docs/GUIA_GRABACION_OBS.md`: perfil, escenas `Camara`, `Clase` y `Pantalla`, filtros del micrófono y atajos
- [ ] Grabar 30 s de prueba en cada escena y revisarlos (luz, sonido y encuadre)
- **Entregable:** un clip de prueba con cambio de escena y audio limpio.

## Fase 2: Cuentas, claves y voces (1 hora)
- [ ] `.env` con `APIMART_API_KEY` y `ELEVENLABS_API_KEY`
- [ ] Verificar rutas y modelos de Apimart (`docs/PROVEEDORES.md`) y rellenar `costos_usd`
- [ ] Elegir en la Voice Library de ElevenLabs las 5 voces (`narrador`, `modelo_en`, `estudiante_us`, `estudiante_uk`, `estudiante_no_nativo`) y pegar sus IDs en `config.yaml`
- [ ] `python builder.py comparar-voces "Hi! I'm your Spanish tutor." --voz modelo_en` → escuchar y ajustar
- **Entregable:** dos audios de prueba que te gustan.

## Fase 3: Materiales e ilustraciones (dry-run gratis → generación)
- [ ] `python builder.py materiales --breve` → revisar el número de llamadas y el coste
- [ ] `python builder.py materiales MAT01 --generar` → **una sola** prueba; revisa la ilustración y el resultado híbrido
- [ ] Si te gusta el estilo: `python builder.py materiales --generar` (ilustraciones de módulo, fondos, materiales y packs de audio)
- [ ] Verifica las horas del mapa MCER (MAT01) y pon `verificado: true`
- **Entregable:** `04_Workbooks/Materiales/` con 9 imágenes finales y `04_Workbooks/Audios/` con 16 pistas.

## Fase 4: Lección piloto M01_L01 (1 día)
Valida la cadena completa con UNA lección antes de producir en serie.
- [ ] Revisar y ajustar el guion (`estado: revisado`)
- [ ] `python builder.py preparar 01 01 --generar` → B-Roll e imágenes de la lección
- [ ] Grabar con el teleprompter → `02_Bruto_OBS/M01_L01_Nicho_RAW.mp4`
- [ ] `python builder.py editar 01 01` → DaVinci: SWA 1 → revisar → SWA 2
- [ ] Anotar ajustes: umbral del Auto-Cut, duración de slides, zoom y estilo visual
- **Entregable:** `05_Renders_Finales/M01_L01_Nicho_FINAL.mp4` que publicarías tal cual.

## Fase 5: Revisión de guiones y assets en lote
- [ ] Leer cada guion en voz alta una vez (unos 4 min cada uno): cambia lo que no suene a ti y resuelve cada `[NOTA: verificar …]`
- [ ] `python builder.py validar` → sin errores
- [ ] Por módulo: `python builder.py preparar MM LL --breve` → `--generar`
- **Entregable:** `python builder.py estado` con todos los assets en `N/N`.

## Fase 6: Grabación por bloques
Un módulo por sesión, misma ropa, luz y encuadre. Cada lección: unos 4 min de lectura, entre 10 y 15 min con tomas repetidas.

| Sesión | Lecciones | Duración aproximada |
|---|---|---|
| 1 | M01 (4) | 1 h |
| 2 | M02 (4) | 1 h |
| 3 | M03 (3) + M07_L01 | 1 h |
| 4 | M04 (4) | 1 h |
| 5 | M05 (3) + M07_L02-L03 | 1 h 15 min |
| 6 | M06 (4) | 1 h |
| 7 | M07_L04-L05 | 30 min |

- **Entregable:** 27 archivos `_RAW.mp4` con el nombre correcto (`python builder.py validar` lo comprueba).

## Fase 7: Postproducción y workbooks
- [ ] Por lección: `editar` → SWA 1 → revisar marcadores (azul = pantalla, rojo = falta asset) → SWA 2
- [ ] Capturas de Lightshot/Flameshot en `03_Assets_Generados/CAPTURAS/M[XX]_L[XX]_*.png`
- [ ] `python builder.py workbook 1` … `7`
- **Entregable:** 27 `_FINAL.mp4` + 7 workbooks PDF.

## Fase 8: Lanzamiento minimalista
- [ ] Skool: aula con videos, workbooks, materiales y audios; comunidad para dudas entre alumnos
- [ ] Checkout (Gumroad o Stripe): curso self-paced como producto de entrada
- [ ] TidyCal: "Auditoría de Perfil 1 a 1" (ya enlazada en cada workbook y en la última lección)
- [ ] `/captacion`: lead magnet (mini-curso del Módulo 1), página de ventas y Shorts "antes y después" con un único CTA
- **Entregable:** embudo Shorts → lead magnet → curso → mentoría funcionando.

---

## Uso eficiente de Claude Code (tokens)
- Contexto de lección: `/guion MM LL` ejecuta `builder.py contexto` (unas 20 líneas) en vez de leer YAML y guiones enteros.
- `/produccion` usa un modelo ligero (Haiku) y no lee archivos generados: le basta la salida de la CLI.
- `/materiales`, `/produccion` y `/captacion` solo se cargan cuando los invocas (`disable-model-invocation`): no ocupan contexto en cada mensaje.
- Todo lo determinista (validar, contar, nombrar, generar visuales y montar) lo hace Python: Claude solo escribe lo creativo.
- Para un módulo entero, pide `/guion MM` en un solo mensaje: el contexto se carga una vez para todas las lecciones.

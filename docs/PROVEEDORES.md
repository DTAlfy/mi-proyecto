# Proveedores de IA: Apimart vs ElevenLabs

## Qué es cada uno

**Apimart** es un *agregador*: con una sola API key y una sola factura te da acceso a cientos de modelos
de otras empresas (imagen: GPT-4o Image, Flux...; video: Sora 2, Wan, Seedance, Flux Video...; además
texto, Whisper y TTS). Su API es compatible con la de OpenAI y las generaciones de video son **asíncronas**:
la petición devuelve un `task_id` y luego hay que consultar el resultado.

**ElevenLabs** es un *especialista en voz*. Su TTS multilingüe es de los más naturales del mercado:
entonación, pausas y emoción. Solo hace audio.

## Reparto en este curso

| Necesidad | Proveedor | Motivo |
|---|---|---|
| B-Roll en video `[BROLL]` | **Apimart** | Un solo saldo para varios modelos; cambias de modelo en `config.yaml` sin tocar código |
| Imágenes `[IMG]` | **Apimart** | Igual que el B-Roll |
| Ilustraciones de módulo y de materiales (MCER, objetivos, plantillas...) | **Apimart + texto local** | Modelo híbrido: ver abajo |
| Slides, roadmap y tarjetas de objetivos | **Local (gratis)** con ilustración de Apimart | Texto exacto a $0 |
| Voces `[AUDIO]` y packs de listening/shadowing | **ElevenLabs** | Te gusta cómo suena; son pocas frases y se reutilizan |
| Transcripción (sincronizar visuales) | **Apimart (Whisper)** | Barato y sin cuenta extra |

La **voz principal del curso es la tuya**: ElevenLabs se usa para frases modelo en inglés y para las
voces de los "alumnos" del módulo Express (listening con distintos acentos).

## Modelo híbrido para imágenes entregables

Los modelos de imagen todavía deforman letras, tildes y cifras. En un mapa MCER, un "DELE B1" mal
escrito o unas horas inventadas no son aceptables en un material que vas a vender. Por eso:

1. **Apimart genera la ilustración** (sin texto): `ilustracion:` en `materiales.yaml` o en `curriculum.yaml`.
2. **El texto exacto se compone en local** (Pillow) con tus colores de marca.
3. Si la ilustración todavía no existe, el layout ocupa todo el ancho: puedes revisar los materiales gratis antes de pagar nada.

Para añadir un material nuevo no hace falta tocar código: copia uno en `materiales.yaml` y elige el
layout (`lista`, `escalera`, `linea_tiempo`, `plantilla` o `roadmap`).

## Voces por papel (ElevenLabs)

En `config.yaml › elevenlabs.voces` asignas un voice ID a cada papel:
`narrador`, `modelo_en` (frases modelo del tutor), `estudiante_us`, `estudiante_uk` y
`estudiante_no_nativo`. En el guion: `[AUDIO: estudiante_uk | Can we use English when I get stuck?]`.
La caché tiene en cuenta el papel: dos voces distintas nunca comparten pista.

## Compara antes de decidir (cuesta 2 frases)

```bash
python builder.py comparar-voces "Hi! I'm your Spanish tutor. Nice to meet you." --voz modelo_en
```
Crea `03_Assets_Generados/AUDIO/_comparacion/elevenlabs.mp3` y `apimart.mp3`. Escúchalos y cambia
`proveedores.tts` en `config.yaml` si prefieres Apimart.

## Antes del primer uso real (pendiente de verificar)

No pude abrir la documentación de Apimart desde el entorno de desarrollo (la red lo bloqueaba). El
código está preparado para el formato compatible con OpenAI que describen sus páginas públicas, pero
**comprueba en https://docs.apimart.ai**:

1. Rutas: `ruta_imagen`, `ruta_video`, `ruta_tarea` (consulta de tareas), `ruta_tts`, `ruta_transcripcion`.
2. Nombres exactos de modelo (`modelo_imagen`, `modelo_video`...) y sus parámetros (`parametros_video`: duración, resolución, aspecto).
3. Si ofrecen TTS (si no, deja `proveedores.tts: elevenlabs`).
4. Tus precios por llamada → `costos_usd` en `config.yaml`, para que el dry-run calcule el coste.

Haz la primera prueba con **una sola** lección: `python builder.py preparar 01 01 --generar`.
El cliente detecta solo dónde viene la URL del resultado, así que suele bastar con ajustar `config.yaml`.

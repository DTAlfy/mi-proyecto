# Proveedores de IA: Apimart vs ElevenLabs

## Qué es cada uno

**Apimart** es un *agregador*: con una sola API key y una sola factura te da acceso a cientos de modelos
de otras empresas (imagen: GPT-4o Image, Flux...; video: Sora 2, Wan, Seedance, Flux Video...; además
texto, Whisper y TTS). Su API es compatible con la de OpenAI y las generaciones de video son **asíncronas**:
la petición devuelve un `task_id` y luego hay que consultar el resultado.

**ElevenLabs** es un *especialista en voz*. Su TTS multilingüe es de los más naturales del mercado:
entonación, pausas y emoción. Solo hace audio.

## Recomendación para este curso

| Necesidad | Proveedor | Motivo |
|---|---|---|
| B-Roll en video | **Apimart** | Un solo saldo para varios modelos; puedes cambiar de modelo en `config.yaml` sin tocar código |
| Imágenes ilustrativas | **Apimart** | Igual que el B-Roll |
| Slides y roadmap | **Local (gratis)** | La IA escribe mal el texto; Pillow lo hace perfecto y a $0 |
| Voz `[AUDIO]` | **ElevenLabs** | Te gusta cómo suena y el volumen es pequeño (pocas frases por lección): el plan más barato suele bastar |
| Transcripción (sincronizar visuales) | **Apimart (Whisper)** | Barato y sin cuenta extra |

La **voz principal del curso es la tuya**: el TTS solo se usa en frases cortas (citas, ejemplos de
alumnos, efectos). Por eso pagar por la mejor voz casi no afecta al presupuesto total.

## Compara antes de decidir (cuesta 2 frases)

```bash
python builder.py comparar-voces "Hola, soy tu nuevo alumno y quiero hablar español en tres meses."
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

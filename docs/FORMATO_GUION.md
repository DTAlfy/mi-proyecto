# Formato de guion

Cada lección es un archivo `01_Guiones/M[XX]_L[XX]_[Clave].md`. El mismo archivo produce el
**teleprompter**, los **visuales**, la **sincronización en DaVinci** y el **workbook**.

## Frontmatter (obligatorio)

```yaml
---
leccion: M01_L01        # debe coincidir con el nombre del archivo
clave: Nicho            # debe coincidir con curriculum.yaml
titulo: "Elige un nicho que pague"
duracion_objetivo_min: 8
estado: borrador        # borrador | revisado | grabado
---
```

## Estructura pedagógica

| Sección | Duración | Qué hace |
|---|---|---|
| 1. Hook | 15 s | Revela un problema crítico que el alumno siente hoy |
| 2. Dónde estamos | 20-30 s | `[ROADMAP]` (posición en la hoja de ruta) + `[OBJETIVOS]` (qué sabrá hacer al terminar) |
| 3. Problema | 1 min | El error habitual y lo que cuesta |
| 4. Solución | 3-4 min | Método en pasos, con `[SLIDE]` |
| 5. Demostración | 1-2 min | `[PANTALLA: ...]` en la plataforma real |
| 6. Tarea | 30 s | Anuncia la `[TAREA]` del workbook |
| 7. Cierre | 20 s | Idea clave + puente a la siguiente lección |

Los títulos `#`/`##` organizan el guion y **no se leen**.

## Etiquetas

| Etiqueta | Genera | Coste | Dónde acaba |
|---|---|---|---|
| `[BROLL: nurse talking patient]` | Video de unos 5 s (Apimart) | $$ | V2 en DaVinci |
| `[IMG: teacher lost in crowd]` | Imagen 16:9 (Apimart) | $ | V2, 5 s |
| `[SLIDE: Título \| punto \| punto]` | PNG local con tu marca | **$0** | V2, 5 s |
| `[ROADMAP]` | Roadmap de Ingresos del módulo, local (fondo opcional de Apimart) | **$0** | V2, 5 s + portada del workbook |
| `[OBJETIVOS: meta \| meta \| meta]` | Tarjeta "En esta clase vas a…" con la ilustración del módulo | **$0** | V2, 5 s |
| `[AUDIO: frase]` | Voz TTS con la voz por defecto | $ | Pausa con tarjeta "Escucha" (V1) + A2 |
| `[AUDIO: estudiante_us \| How long…?]` | Voz TTS con un papel de `config.yaml` (narrador, modelo_en, estudiante_us, estudiante_uk, estudiante_no_nativo) | $ | Igual |
| `[PANTALLA: abre Preply y filtra]` | Nada: aviso para ti al grabar | $0 | Teleprompter, checklist y marcador azul |
| `[NOTA: verificar dato]` | Nada | $0 | Teleprompter y marcador amarillo |
| `[TAREA: título] ... [/TAREA]` | Bloque del workbook (no se lee) | $0 | PDF del módulo |
| `[RECURSO: título] ... [/RECURSO]` | Bloque del workbook (no se lee) | $0 | PDF del módulo |

La etiqueta se coloca **justo donde debe aparecer el visual**: el pipeline mide en qué palabra está
y la sincroniza con tu voz grabada.

**Los `[AUDIO]` se intercalan**: en la edición el video se detiene en una tarjeta «Escucha» mientras suena
la pista y después continúa. Al grabar no hace falta hacer pausas.

**Escenas de OBS**: no hacen falta etiquetas. El teleprompter indica *Camara* al empezar, *Clase* en cada
`[PANTALLA]` y vuelta a *Camara* en el siguiente título.

## Reglas de estilo
- Frases de 20 palabras como máximo. Una idea por párrafo. Habla a una persona: *tú*.
- Prompts visuales en **inglés**, de 3 a 6 palabras: sujeto + acción + contexto. Sin texto ni logos (el estilo de marca se añade solo desde `config.yaml`).
- Todo lo que sea texto en pantalla va en `[SLIDE]`, no en `[IMG]`: la IA escribe mal.
- Como máximo 2 `[BROLL]` y 2 `[IMG]` por lección: son los assets de pago (el video es el más caro).
- Nada de cifras inventadas. Si hace falta un dato, usa `[NOTA: verificar ...]`.

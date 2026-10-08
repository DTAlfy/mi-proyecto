---
name: guion
description: Escribe o mejora guiones de lecciones del curso (una lección o un módulo entero) con la estructura y etiquetas del pipeline.
argument-hint: "MM [LL]"
---

# /guion $ARGUMENTS

1. Ejecuta `python builder.py contexto $ARGUMENTS` (ya trae el currículo, los vecinos, el cierre anterior, los materiales y las voces). No abras los YAML ni otros guiones salvo que el contexto no baste.
2. Escribe cada guion en `01_Guiones/M[MM]_L[LL]_[Clave].md` de una sola vez (Write, sin borradores intermedios).
3. `python builder.py validar MM LL`. Corrige solo lo que marque y no vuelvas a leer el archivo entero para comprobarlo.
4. Responde con una línea por lección: palabras, minutos y visuales de pago (BROLL/IMG/AUDIO).

## Formato (estricto)
Frontmatter: `leccion`, `clave`, `titulo`, `modulo`, `objetivo`, `duracion_objetivo_min`, `estado: borrador`.
Secciones `##`: 1 Hook (15 s, problema crítico) · 2 Dónde estamos (`[ROADMAP]` + `[OBJETIVOS: meta | meta | meta]`) · 3 Problema · 4 Solución (método en pasos, `[SLIDE: Título | punto | punto]`) · 5 Demostración (`[PANTALLA: qué abrir]`) · 6 Tarea (`[TAREA: título]…[/TAREA]` + `[RECURSO: título]…[/RECURSO]`) · 7 Cierre (idea clave + puente a la siguiente).
- Entre 950 y 1.150 palabras leídas. Frases de 20 palabras como máximo, tú, español neutro.
- Visuales cada 20-30 s. Máximo 2 `[BROLL]` y 2 `[IMG]` (prompts en inglés, de 3 a 6 palabras, sin texto). Todo texto en pantalla va en `[SLIDE]`.
- `[AUDIO: papel | frase]` solo cuando aporte (frases modelo, preguntas de alumnos). Reutiliza literalmente las líneas de los packs de audio que da el contexto.
- Sin cifras inventadas: `[NOTA: verificar …]`.
- Módulo Express de inglés: explica en español, el inglés solo en `[AUDIO]`/`[SLIDE]`, nivel sencillo (A2-B1).

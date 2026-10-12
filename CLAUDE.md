# CLAUDE.md — Reglas de la bóveda "Segundo Cerebro de Español"

Esta es una bóveda de Obsidian para enseñar español: clases particulares, Curso de Nuevos Tutores
(producto principal), contenido para redes/Skool, flashcards y futuros cursos para angloparlantes.
El plan completo y las decisiones están en `HANDSHAKE.md`. Léelo si dudas de dónde va algo.

## Idioma
- Escribe siempre en **español**. Términos en inglés solo cuando el contenido es para angloparlantes.

## Estructura (no inventes carpetas nuevas sin preguntar)
| Carpeta | Contenido |
|---|---|
| `00_Inbox/` | Captura rápida sin clasificar |
| `10_Fuentes/` | Material bruto. **Solo lectura**: nunca edites ni borres aquí |
| `20_Conocimiento/<Area>/` | Notas atómicas: `Gramatica`, `Vocabulario`, `Funciones`, `Pronunciacion`, `Cultura`, `Pedagogia` |
| `30_Curriculum/MCER/` | Descriptores por nivel |
| `30_Curriculum/Unidades/<Nivel>/` | Unidades del roadmap `A1.03 Título` |
| `40_Clases/Planes/` | Planes de clase reutilizables |
| `40_Clases/Materiales/` | Fichas, HTML, PDF para clase |
| `50_Cursos/Curso_Tutores/` | Curso principal (módulos `M0`–`M9`) |
| `50_Cursos/Curso_Estudiantes_EN/` | Curso futuro para angloparlantes |
| `60_Estudiantes/{Alumnos,Sesiones,Evaluaciones}/` | Datos de alumnos (privados) |
| `70_Contenido/{Ideas,Produccion,Publicado,Lead_magnets}/` | Pipeline de contenido |
| `90_Archivo/` | Archivo |
| `99_Sistema/` | Plantillas, Bases, Taxonomía, scripts |

## Reglas obligatorias
1. **Propiedades primero.** Toda nota nueva empieza con el frontmatter de su plantilla en
   `99_Sistema/Plantillas/`. Los valores permitidos están en `99_Sistema/Taxonomia.md`. No inventes valores.
2. **Una idea, un lugar.** Antes de crear una nota en `20_Conocimiento`, busca si ya existe
   (por título y alias). Si existe, amplíala; no dupliques.
3. **Enlaza siempre.** Cada concepto enlaza a su unidad del roadmap y a sus fuentes. Cada sesión enlaza
   al alumno, la unidad y los conceptos vistos. Cada pieza de contenido enlaza a su concepto de origen.
4. **Nombres de archivo.** Título natural en español con tildes (`Ser vs estar.md`).
   Unidades: `A2.05 Título.md`. Sesiones: `AAAA-MM-DD Nombre Alumno.md`. Contenido: `AAAA-MM-DD plataforma - título.md`.
5. **Flashcards.** Van en la sección `## Flashcards` de la nota de concepto, una por línea:
   `frente :: reverso`. Máximo una idea por tarjeta.
6. **Bitácora.** Al terminar una tarea que cambie la bóveda, añade una línea en `log.md`:
   `- AAAA-MM-DD — qué se hizo — notas afectadas`.
7. **Privacidad.** No copies datos de alumnos fuera de `60_Estudiantes/`. No subas libros con copyright.

## Tareas frecuentes
- **"Ingiere esta fuente"** → crea la ficha en `10_Fuentes`, recorre sus temas y crea o amplía conceptos en
  `20_Conocimiento` (flujo A del handshake). Informa de las notas creadas y ampliadas.
- **"Registra la sesión de X"** (con capturas o notas) → crea la sesión con la plantilla, enlaza los conceptos
  y actualiza `ultima_sesion` en la ficha del alumno.
- **"Evalúa a X"** → crea la evaluación y actualiza `nivel_actual`, `unidad_actual` y `progreso` en la ficha.
- **"Convierte el Sheet/CSV en fichas"** → una ficha por alumno con la plantilla Alumno.
- **"Saca contenido de `[[Ser vs estar]]`"** → 1 pieza pilar + derivadas por plataforma, con la plantilla
  Pieza de contenido, en `70_Contenido/Produccion/`.
- **"Prepara la lección MX.Y del curso de tutores"** → plantilla Lección de curso; se apoya en `20_Conocimiento/Pedagogia`.
- **"Exporta flashcards"** → `python 99_Sistema/scripts/exportar_flashcards.py --nivel A1`.

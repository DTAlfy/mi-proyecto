# CLAUDE.md — Reglas de la bóveda "Segundo Cerebro de Español"

Esta es una bóveda de Obsidian para enseñar español: clases particulares, Curso de Nuevos Tutores
(producto principal), contenido para redes/Skool, flashcards y futuros cursos para angloparlantes.
El plan completo y las decisiones están en `HANDSHAKE.md`. Léelo si dudas de dónde va algo.

**Método:** 80 % práctica con situaciones (misiones) con goals medibles, 20 % input. La columna vertebral es el
**árbol de habilidades** (`30_Curriculum/Arbol/`): nodos de situación (S), gramática (G) y vocabulario (V)
unidos por `requiere`. El progreso de cada alumno se calcula con `99_Sistema/scripts/arbol.py`.

## Idioma
- Escribe siempre en **español**. Términos en inglés solo cuando el contenido es para angloparlantes.

## Estructura (no inventes carpetas nuevas sin preguntar)
| Carpeta | Contenido |
|---|---|
| `00_Inbox/` | Captura rápida sin clasificar |
| `10_Fuentes/` | Material bruto. **Solo lectura**: nunca edites ni borres aquí |
| `20_Conocimiento/<Area>/` | Notas atómicas: `Gramatica`, `Vocabulario`, `Funciones`, `Pronunciacion`, `Cultura`, `Pedagogia` |
| `30_Curriculum/Arbol/<Nivel>/` | Nodos del árbol: `A1.S07 Título` (S situación, G gramática, V vocabulario) |
| `30_Curriculum/MCER/` | Descriptores oficiales de referencia |
| `40_Clases/Planes/` | Planes de clase reutilizables |
| `40_Clases/Materiales/` | Materiales con `nodos:` (se desbloquean con el árbol) |
| `50_Cursos/Curso_Tutores/` | Curso principal (módulos `M0`–`M9`) |
| `50_Cursos/Curso_Estudiantes_EN/` | Curso futuro para angloparlantes |
| `60_Estudiantes/{Alumnos,Sesiones,Evaluaciones}/` | Datos de alumnos (privados) |
| `60_Estudiantes/Arboles/` | **Generado** por `arbol.py`. No editar a mano |
| `70_Contenido/{Ideas,Produccion,Publicado,Lead_magnets}/` | Pipeline de contenido |
| `90_Archivo/` | Archivo |
| `99_Sistema/` | Plantillas, Bases, Taxonomía, scripts |

## Reglas obligatorias
1. **Propiedades primero.** Toda nota nueva empieza con el frontmatter de su plantilla en
   `99_Sistema/Plantillas/`. Los valores permitidos están en `99_Sistema/Taxonomia.md`. No inventes valores.
2. **Una idea, un lugar.** Antes de crear una nota en `20_Conocimiento`, busca si ya existe
   (por título y alias). Si existe, amplíala; no dupliques.
3. **Enlaza siempre.** Cada concepto enlaza a sus nodos (`nodos:`) y fuentes; cada nodo a sus conceptos (`conceptos:`).
   Cada sesión enlaza al alumno y a los nodos (`practicados`, `logrados`). Cada pieza de contenido enlaza a su origen.
4. **Nombres de archivo.** Título natural en español con tildes (`Ser vs estar.md`). **Nunca** uses `: * ? " < > | # ^ [ ]`
   (Windows/Obsidian no los permiten; usa ` - `). Nodos: `A2.S05 Título.md`. Sesiones: `AAAA-MM-DD Nombre Alumno.md`.
   Contenido: `AAAA-MM-DD plataforma - título.md`.
5. **Flashcards.** Van en la sección `## Flashcards` de la nota de concepto, una por línea:
   `frente :: reverso`. Máximo una idea por tarjeta.
6. **Bitácora.** Al terminar una tarea que cambie la bóveda, añade una línea en `log.md`:
   `- AAAA-MM-DD — qué se hizo — notas afectadas`.
7. **Privacidad.** No copies datos de alumnos fuera de `60_Estudiantes/`. No subas libros con copyright.
8. **El árbol.** `requiere` lleva solo los requisitos **directos**. Tras cambiar nodos, ejecuta
   `python 99_Sistema/scripts/arbol.py --validar`. Tras registrar sesiones o evaluaciones, ejecuta `arbol.py`.
   Un nodo es `logrado` solo si el alumno cumplió **todos** sus goals sin ayuda; si no, va en `practicados`.
9. **Antes de mover o borrar** carpetas de la bóveda, propón el plan y espera confirmación.

## Tareas frecuentes
- **"Ingiere esta fuente"** → crea la ficha en `10_Fuentes`, recorre sus temas y crea o amplía conceptos en
  `20_Conocimiento` (flujo A del handshake). Informa de las notas creadas y ampliadas.
- **"Registra la sesión de X"** (con capturas o notas) → crea la sesión con la plantilla, rellena `practicados` y
  `logrados` con nodos del árbol, pega las capturas dentro y ejecuta `arbol.py`. Resume cómo cambió su árbol.
- **"Evalúa a X"** → crea la evaluación con `logrados` y la escala 1-5 y ejecuta `arbol.py`.
- **"Convierte el Sheet/CSV en fichas"** → una ficha por alumno con la plantilla Alumno; para antiguos propón
  `nivel_base` y `meta` y pregunta lo que no sepas.
- **"¿Cómo va X?" / "¿Qué hago hoy con X?"** → lee su nota `<X> - Ruta` y propone la clase con la siguiente situación.
- **"Crea una situación / un nodo"** → plantilla *Situación (misión)* o *Habilidad*, con `requiere` y goals medibles; valida.
- **"Saca contenido de `[[Ser vs estar]]`"** → 1 pieza pilar + derivadas por plataforma, con la plantilla
  Pieza de contenido, en `70_Contenido/Produccion/`.
- **"Prepara la clase de `[[A2.S05 Pregunta por un piso en alquiler]]`"** → *Plan de clase* 80/20 en `40_Clases/Planes/` + materiales con `nodos:`.
- **"Prepara la lección MX.Y del curso de tutores"** → plantilla Lección de curso; se apoya en `20_Conocimiento/Pedagogia`.
- **"Exporta flashcards"** → `python 99_Sistema/scripts/exportar_flashcards.py --nivel A1`.

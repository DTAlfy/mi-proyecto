# 🤝 Handshake — Segundo Cerebro de Español

> Documento de acuerdo entre tú y Claude: **qué construimos, por qué, y cómo se usa**.
> Si algo cambia, se cambia aquí primero y luego en `CLAUDE.md`.

---

## 1. Objetivo

Un **esqueleto absoluto**: una sola estructura donde todo el material y conocimiento de español
vive **una vez** y se reutiliza para:

| Salida | Para quién | Prioridad |
|---|---|---|
| 🎓 **Curso de Nuevos Tutores de Español** | Nativos que quieren empezar a enseñar | **Principal** |
| 📚 Clases particulares | Tus alumnos actuales y antiguos | Continua |
| 📣 Contenido en redes + Skool | Tutores y estudiantes (todas las plataformas) | Continua |
| 🃏 Flashcards | Alumnos y tutores | Futuro (ya preparado) |
| 🇬🇧 Cursos ultrasólidos para angloparlantes (A0→B2) | Estudiantes de inglés nativo | Futuro (ya preparado) |

**Problema que resolvemos:**
- El material está importado pero **no conectado** (los "racimos" aislados del grafo).
- El progreso de alumnos vive en **capturas de pantalla + un Google Sheet** desordenado.
- Cada pieza de contenido se crea desde cero en vez de **derivarse** de lo que ya sabes.

---

## 2. Principios (las reglas del juego)

1. **Una idea, un lugar.** Cada concepto (p. ej. *Ser vs estar*) existe en **una** nota de `20_Conocimiento`.
   Clases, cursos, posts y flashcards **enlazan** a esa nota; no la copian.
2. **El MCER es la columna vertebral.** Todo lleva `nivel` (A0–B2, o `tutor`). Así el grafo se
   ordena por niveles y el progreso se puede medir.
3. **Las fuentes no se tocan.** `10_Fuentes` es material bruto (libros, PDFs, capturas). Se lee,
   se extrae, se cita, pero no se edita.
4. **Metadatos obligatorios.** Cada nota empieza con propiedades (`tipo`, `nivel`, `estado`…)
   definidas en [[99_Sistema/Taxonomia|Taxonomía]]. Sin propiedades, los tableros no la ven.
5. **Crear con plantilla, siempre.** Nada se escribe en blanco: se usa la plantilla del tipo de nota.
6. **Producir = derivar.** Un concepto → una clase → una lección de curso → 5-10 piezas de contenido → flashcards.
7. **Privacidad.** Los datos de alumnos y los libros con copyright **no se suben** al repositorio (ver `.gitignore`).

---

## 3. Arquitectura

```
00_Inbox/          Captura rápida. Todo entra aquí si no sabes dónde va. Se vacía cada semana.
10_Fuentes/        Material bruto: libros, PDFs, epubs, manuales DELE, capturas, exports de Sheets.
20_Conocimiento/   La WIKI. Notas atómicas por concepto:
   ├─ Gramatica/      ser vs estar, subjuntivo, pasados…
   ├─ Vocabulario/    campos léxicos por tema
   ├─ Funciones/      pedir, opinar, quejarse… (funciones comunicativas)
   ├─ Pronunciacion/  sonidos, entonación, errores típicos de angloparlantes
   ├─ Cultura/        variedades, costumbres, referentes
   └─ Pedagogia/      CÓMO enseñar: metodología, corrección, planificación, negocio (→ curso tutores)
30_Curriculum/     El ROADMAP medible:
   ├─ MCER/           descriptores "puedo hacer…" por nivel (A0, A1, A2, B1, B2)
   └─ Unidades/       A0.01 … B2.12 — cada unidad enlaza a conceptos de la wiki
40_Clases/         Planes de clase reutilizables + materiales (fichas, HTML, PDF)
50_Cursos/
   ├─ Curso_Tutores/          ⭐ PRINCIPAL — módulos y lecciones para Skool
   └─ Curso_Estudiantes_EN/   futuro — se construye sobre 30_Curriculum
60_Estudiantes/    Fichas de alumnos, sesiones, evaluaciones (privado, no se sube)
70_Contenido/      Línea de producción: Ideas → Producción → Publicado (+ Lead magnets)
90_Archivo/        Lo que ya no se usa pero no quieres borrar
99_Sistema/        Plantillas, Tableros (.base), Taxonomía, scripts
```

**Archivos raíz:** `CLAUDE.md` (reglas para Claude) · `Inicio.md` (tu panel principal) ·
`log.md` (bitácora de cambios) · `HANDSHAKE.md` (este documento).

### Cómo se conecta todo

```
10_Fuentes ──extraer──▶ 20_Conocimiento ──agrupar──▶ 30_Curriculum (Unidades por nivel)
                              │                              │
                              │                              ├──▶ 40_Clases (plan de clase)
                              │                              │         │
                              │                              │         └──▶ 60_Estudiantes (sesión → progreso)
                              │                              │
                              ├──enseñar a enseñar──▶ 50_Cursos/Curso_Tutores
                              │
                              ├──derivar──▶ 70_Contenido (reels, carruseles, posts Skool, PDFs, HTML)
                              │
                              └──extraer──▶ Flashcards (sección "## Flashcards" de cada nota)
```

---

## 4. Los 5 flujos de trabajo

### A. Ingerir una fuente (romper los racimos)
1. El libro/PDF va a `10_Fuentes/` con su ficha (plantilla **Fuente**).
2. Claude (o tú) recorre el índice del libro y, por cada tema, **busca si ya existe** la nota en `20_Conocimiento`.
   - Si existe → añade la referencia a la fuente (`fuentes:`) y lo nuevo que aporte.
   - Si no existe → crea la nota con la plantilla **Concepto**.
3. Resultado: el libro deja de ser una "estrella aislada" y sus temas se unen a la red.

### B. Preparar una clase
1. Abres la **Unidad** del roadmap (p. ej. `A2.05`).
2. Creas un **Plan de clase** en `40_Clases/Planes/` que enlaza a la unidad y a los conceptos.
3. El plan se reutiliza con cada alumno que llegue a esa unidad.

### C. Registrar una sesión (adiós capturas sueltas)
1. Tras la clase: nota **Sesión** en `60_Estudiantes/Sesiones/` → alumno, unidad, temas, errores, tarea.
2. Las capturas de pantalla se pegan **dentro** de la sesión (ya no sueltas).
3. Cada 4-6 sesiones: **Evaluación** → actualiza `nivel_actual`, `unidad_actual` y `progreso` en la ficha.
4. El tablero **Alumnos** muestra a todos (activos, en pausa, antiguos) de un vistazo.

### D. Producir contenido (1 idea → muchas piezas)
1. Idea en `70_Contenido/Ideas/` (plantilla **Idea**), enlazada a un concepto.
2. Se elige una **pieza pilar** (lección Skool o vídeo largo).
3. Se derivan piezas por plataforma (plantilla **Pieza de contenido**): reel/TikTok/Short, carrusel,
   post de Skool, email, PDF (NotebookLM) o HTML (Claude).
4. El tablero **Contenido** muestra el pipeline: idea → guion → producción → programado → publicado.

### E. Flashcards
- Cada nota de concepto tiene una sección `## Flashcards` con líneas `frente :: reverso`.
- Funcionan dentro de Obsidian (plugin *Spaced Repetition*) y se exportan a Anki con
  `python 99_Sistema/scripts/exportar_flashcards.py`.

---

## 5. Migración desde tu bóveda actual

| Carpeta actual | Destino |
|---|---|
| `A1Hidalgo_Andrea_Fabiana_-_Preparaci…` | `10_Fuentes/Libros/` |
| `DELE_B2_Preparación_BLANCO_Y_NEGR…` | `10_Fuentes/Libros/` |
| `Lazlo_Sandor_-_Tiempo…_Para_practicar…` | `10_Fuentes/Libros/` |
| `Libros de ESPAÑOL Alfy` | `10_Fuentes/Libros/` |
| `Epubs` | `10_Fuentes/Epubs/` |
| `raw` | `10_Fuentes/` (revisar contenido) |
| `wiki` | `20_Conocimiento/` (reclasificar por área) |
| `MCER` / `MCER Markdown` | `30_Curriculum/MCER/` (fusionar con los descriptores nuevos) |
| `ideas` | `70_Contenido/Ideas/` (o `00_Inbox` si están sin procesar) |
| `plantillas` | `99_Sistema/Plantillas/` (fusionar con las nuevas) |
| `scripts` | `99_Sistema/scripts/` |
| `CLAUDE`, `index`, `log` | raíz → fusionar con `CLAUDE.md`, `Inicio.md`, `log.md` |
| `Untitled`, `Untitled.base` | revisar → borrar o mover a `99_Sistema/Bases/` |
| Google Sheet de alumnos | exportar a CSV → `10_Fuentes/Sheets/` → Claude genera una ficha por alumno |
| Capturas de clases | `10_Fuentes/Capturas_clases/<alumno>/` → se enlazan desde las sesiones |

> ⚠️ Mueve las carpetas **desde dentro de Obsidian** (arrastrar en el explorador) para que
> los enlaces se actualicen solos.

---

## 6. Plan por fases

| Fase | Qué | Resultado |
|---|---|---|
| **0. Esqueleto** ✅ | Estructura, taxonomía, plantillas, tableros, roadmap, curso tutores | Este repositorio |
| **1. Migrar** | Mover tu bóveda actual a la nueva estructura (tabla de arriba) | Todo en su sitio |
| **2. Alumnos** | Sheet → fichas; capturas → sesiones; primera evaluación de cada activo | Tablero de progreso real |
| **3. Conectar fuentes** | Flujo A con cada libro, empezando por los de A1 y B2 | Grafo conectado por niveles |
| **4. Curso de Tutores** | Rellenar módulos M0–M9 desde `20_Conocimiento/Pedagogia` | Curso listo para Skool |
| **5. Máquina de contenido** | Pilares + calendario + derivación por plataforma | Publicación constante |
| **6. Flashcards** | Secciones `## Flashcards` + export a Anki | Mazos por nivel |
| **7. Curso EN** | Curso para angloparlantes sobre el roadmap A0→B2 | Segundo producto |

---

## 7. Preguntas abiertas (para la siguiente ronda)

- [ ] ¿Qué plataformas exactas usas y con qué frecuencia quieres publicar en cada una?
- [ ] ¿Tu Skool ya existe? ¿Gratis + de pago, o solo de pago?
- [ ] ¿Qué escala de evaluación prefieres: 1-5 por destreza, o porcentaje de descriptores logrados?
- [ ] ¿Usarás Claude Code en tu PC sobre la bóveda, o subiremos la bóveda a este repo (privado)?
- [ ] ¿Cuál es tu "método" o diferencial como profe? (Es el corazón del Curso de Tutores.)

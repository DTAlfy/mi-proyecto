# 🖥️ Plan para organizar tu segundo cerebro en tu PC

> **Idea principal:** organizar y **conectar** todos los materiales que usas, para **dar clases**, **crear cursos**
> y **generar contenido** desde un solo lugar, con el sistema del [[HANDSHAKE]] (Método Misiones 80/20 + árbol de habilidades).
>
> **Cómo se usa:** haces 4 pasos a mano (unos 15 minutos), abres Claude Code en tu bóveda y pegas el **prompt maestro**.
> Claude trabaja por fases y se para en cada punto de control ⏸️ para que apruebes antes de mover nada.

---

## 1. Antes de pegar (a mano, una sola vez)

1. **Instala** (si no los tienes):
   - **Claude Code**: app de escritorio o terminal. Instrucciones oficiales en `code.claude.com`.
   - **Git**: `git-scm.com`.
   - **Python 3**: `python.org`. En Windows, marca **"Add Python to PATH"** al instalar.
2. **Cierra Obsidian.** Claude te avisará cuando puedas abrirlo.
3. **Abre Claude Code en la carpeta de tu bóveda** (la que Obsidian llama *Second Brain*).
4. **Pega el prompt maestro** (abajo). Claude te pedirá permiso para ejecutar comandos y mover archivos: revisa y acepta.

> 💡 La conversación va a ser larga. Si en algún momento Claude va lento o la sesión se corta, abre una sesión nueva
> y pega el **prompt de continuación** (sección 3). Claude sabrá por dónde iba gracias a
> `99_Sistema/Organizacion - progreso.md`.

---

## 2. Prompt maestro (copia todo el bloque)

```text
Eres mi asistente para organizar mi segundo cerebro de Obsidian. Esta carpeta es mi bóveda.

OBJETIVO: organizar y CONECTAR todos mis materiales de español (libros, wiki, ideas, MCER, plantillas, capturas de
clases, datos de alumnos) para poder (1) dar clases, (2) crear cursos — el Curso de Nuevos Tutores y, en el futuro,
cursos para angloparlantes A0-B2 — y (3) generar contenido para todas las redes y Skool. Vamos a implantar el sistema
diseñado en el repositorio de GitHub DTAlfy/mi-proyecto, rama claude/festive-feynman-6dy8ui (lo llamo "el esqueleto"):
Método Misiones 80/20 (situaciones con goals medibles) + árbol de habilidades A0-B2 + plantillas, tableros y scripts.

REGLAS DURANTE TODO EL PROCESO
1. Nunca borres nada. Lo que sobre va a 90_Archivo/.
2. Para migrar, MUEVE (no copies). Solo se copia el esqueleto.
3. En cada punto marcado con ⏸️ enséñame el plan o el resultado y ESPERA mi "OK" antes de seguir.
4. No edites el contenido de los libros ni de las fuentes. Se conectan desde fuera (conceptos, materiales, fichas).
   Única excepción: arreglar la ruta de un enlace que se rompió al mover carpetas.
5. Obsidian debe estar cerrado cuando muevas carpetas o toques .obsidian. Avísame cuando pueda abrirlo.
6. Desde la Fase 1, lleva el progreso en 99_Sistema/Organizacion - progreso.md (casillas, tablas, decisiones)
   para poder continuar en otra sesión. Al cerrar cada fase, añade una línea en log.md.
7. Respeta CLAUDE.md del esqueleto: propiedades de las plantillas, valores de 99_Sistema/Taxonomia.md, nombres de
   archivo sin : * ? " < > | # ^ [ ], una idea en un solo lugar, enlazar siempre.
8. Si algo falla o dudas, para y pregúntame. En Windows, si `python` no funciona, usa `py`.

FASE 0 — Seguridad e inventario ⏸️
a) Crea una copia de seguridad .zip de toda esta carpeta FUERA de ella (p. ej. en Documentos/Backups/
   SecondBrain-AAAA-MM-DD.zip). Comprueba que existe y dime su tamaño.
b) Descarga el esqueleto en una carpeta FUERA de la bóveda (p. ej. Documentos/esqueleto-segundo-cerebro):
   git clone --branch claude/festive-feynman-6dy8ui https://github.com/DTAlfy/mi-proyecto.git <esa carpeta>
   Si falla (el repositorio es privado y pide acceso), pídeme que descargue el ZIP de esa rama desde GitHub y te diga
   dónde lo dejé.
c) Lee del esqueleto: HANDSHAKE.md, CLAUDE.md, PLAN_PC.md, 99_Sistema/Taxonomia.md,
   "30_Curriculum/Árbol de habilidades A0-B2.md", "50_Cursos/Escalera de productos.md" y
   "70_Contenido/Estrategia de contenido.md". Ese es el sistema que vamos a implantar.
d) Inventario de mi bóveda actual con el script del esqueleto:
   python "<esqueleto>/99_Sistema/scripts/revisar_boveda.py" --boveda "." --salida "<esqueleto>/inventario_antes.md"
e) Explora cada carpeta de primer nivel (lee varias notas de cada una, sobre todo las notas centrales/hubs del
   inventario) y averigua qué es cada una: libro convertido, wiki, ideas, plantillas, scripts, etc. Mira también
   cómo están escritos los enlaces (solo nombre [[Nota]] o con ruta [[carpeta/Nota]]), porque eso decide si mover
   rompe enlaces.
f) Enséñame: (1) resumen del inventario (notas, carpetas aisladas, enlaces rotos); (2) la tabla
   "carpeta actual → destino" usando HANDSHAKE.md §5 como base, con nombres de carpeta cortos para cada libro
   (p. ej. 10_Fuentes/Libros/A1 Hidalgo); (3) lo que no sabes dónde va. ⏸️

FASE 1 — Instalar el esqueleto ⏸️ (Obsidian cerrado)
a) Copia del esqueleto a la bóveda: las carpetas 00_Inbox … 99_Sistema y los archivos HANDSHAKE.md, PLAN_PC.md,
   Inicio.md, CLAUDE.md, log.md, README.md y .gitignore. NO copies .git. NO sobrescribas ningún archivo mío.
b) Conflictos: si ya existen mi CLAUDE.md, log.md o index.md, muévelos antes a 90_Archivo/Sistema_anterior/.
   Después instala los del esqueleto. Añade al final del nuevo CLAUDE.md una sección "## Reglas heredadas" con lo que
   siga siendo útil de mi CLAUDE anterior (sin contradecir lo nuevo) y en log.md una línea que enlace al log anterior.
c) Obsidian: guarda una copia de .obsidian/graph.json y .obsidian/templates.json en
   90_Archivo/Sistema_anterior/obsidian/. Luego, en mi graph.json AÑADE los colorGroups del esqueleto (sin quitar
   los míos) y pon "showArrow": true. En templates.json pon "folder": "99_Sistema/Plantillas" (créalo si no existe).
d) Mi carpeta de plantillas antigua → 99_Sistema/Plantillas/Anteriores/. Mis scripts → 99_Sistema/scripts/Anteriores/.
e) Ejecuta: python 99_Sistema/scripts/arbol.py --validar   y después   python 99_Sistema/scripts/arbol.py
f) Rellena la tabla de destinos aprobada en 99_Sistema/Organizacion - progreso.md y marca las fases 0 y 1.
g) Dime que ya puedo abrir Obsidian para comprobar Inicio.md, el grafo (colores por tipo),
   30_Curriculum/Arbol maestro.canvas y 60_Estudiantes/Arboles/Demo Emma.html. Pídeme que active los plugins núcleo
   Bases, Canvas, Plantillas y Propiedades si no lo están. ⏸️

FASE 2 — Migrar ⏸️ (Obsidian cerrado)
a) Línea base: python 99_Sistema/scripts/revisar_boveda.py --enlaces  (apunta cuántos rotos hay ANTES de mover).
b) Mueve según la tabla aprobada. Cada libro va a 10_Fuentes/Libros/<nombre corto>/ conservando su estructura
   interna; Epubs → 10_Fuentes/Epubs/; raw → 10_Fuentes/Otros/ (o donde corresponda); wiki → 20_Conocimiento/<Area>/
   según el tema de cada nota (si dudas → 00_Inbox/); ideas → 70_Contenido/Ideas/; MCER → 30_Curriculum/MCER/;
   Untitled y sueltos → 00_Inbox/.
c) Después: revisar_boveda.py --enlaces otra vez. Si hay enlaces rotos NUEVOS por rutas que cambiaron, corrígelos
   (solo la ruta del enlace). Objetivo: igual o menos rotos que antes.
d) Guarda el informe: python 99_Sistema/scripts/revisar_boveda.py --salida 00_Inbox/inventario_tras_migrar.md
e) Enséñame qué se movió, los enlaces arreglados y lo que quedó en 00_Inbox. ⏸️

FASE 3 — Fichas de fuentes
Para cada libro/fuente crea una ficha en 10_Fuentes/Fichas/ con la plantilla Fuente: qué es, autor, nivel, enlace
a su nota índice y su índice de temas, un tema por línea:  - [ ] Tema → [[nota del capítulo]]
Rellena la tabla "Fuentes" en la nota de progreso. Dime cuántas fichas y temas hay y en qué orden propones
conectarlas (sugerencia: primero las notas de la antigua wiki, luego A1 Hidalgo, DELE B2, Lazlo Sandor y el resto).

FASE 4 — Conectar (el corazón) ⏸️ al terminar CADA fuente
4.0 Primero, las notas que vinieron de la antigua wiki: ponles las propiedades de la plantilla Concepto (area, nivel,
    nodos, fuentes, estado), enlázalas a sus nodos del árbol y fusiona las que dupliquen la misma idea.
4.1 Después, una fuente por ronda (si tiene más de 25 temas, hazla en tandas de unos 20 y guarda el progreso).
    Para cada tema de la ficha:
    1. Decide a qué nodo(s) del árbol sirve: gramática (G), vocabulario (V) o situación (S), y su nivel.
    2. Crea o amplía la nota de concepto en 20_Conocimiento/<Area>/ (plantilla Concepto; una idea en un solo lugar):
       explicación breve con tus palabras, ejemplos, errores típicos de angloparlantes, cómo enseñarlo y 3-5
       flashcards. En `fuentes:` enlaza la ficha y el capítulo exacto. No copies textos largos del libro: resume y
       enlaza.
    3. Añade ese concepto al `conceptos:` del nodo.
    4. Si el capítulo tiene ejercicios, lecturas o audios útiles para clase → nota Material en 40_Clases/Materiales/
       (plantilla Material) con `nodos:` y enlace al capítulo.
    5. Si ves una buena idea de contenido (un error típico, un truco, una situación) → nota en 70_Contenido/Ideas/
       (plantilla Idea) con `origen:`.
    6. Si el material muestra una situación real que no está en el árbol, apúntala en "Decisiones y dudas" de la
       nota de progreso (se decide en la Fase 6).
    7. Marca el tema ✓ en la ficha.
    Al cerrar la fuente: arbol.py --validar, revisar_boveda.py --enlaces, actualiza la nota de progreso y enséñame:
    conceptos creados/ampliados, materiales, ideas y cuántos enlaces entran ahora a la carpeta del libro desde fuera
    (antes era 0). ⏸️

FASE 5 — Alumnos ⏸️
a) Pídeme el CSV de mi Google Sheet de alumnos (yo lo exporto a 10_Fuentes/Sheets/). Crea una ficha por alumno con la
   plantilla Alumno. Para los antiguos, propón `nivel_base` y `meta`; pregúntame lo que no sepas.
b) Pídeme que deje las capturas de clase en 10_Fuentes/Capturas_clases/<alumno>/. Lee las imágenes y crea las sesiones
   (plantilla Sesión): fecha, lo trabajado como `practicados` y solo lo claramente conseguido como `logrados`
   (si dudas → practicados), con la captura insertada en la nota.
c) Propón mover los alumnos Demo (Emma, Jake, Lucía) y sus sesiones a 90_Archivo/Demo/. ⏸️
d) Ejecuta arbol.py y enséñame el resumen del Panel de progreso.

FASE 6 — Ajustar el árbol a mi método ⏸️
Con lo que aprendiste de mis libros y clases, propón: situaciones nuevas con misión y goals medibles (por nivel), cambios
en `requiere`, y qué nodos pasan a `en_desarrollo` o `lista`. Espera mi OK, aplica y valida con arbol.py --validar.

FASE 7 — Activar producción
a) Lead magnet "10 situaciones listas para tu primera clase" en 70_Contenido/Lead_magnets/ (misión, goals y mini plan
   80/20 de cada una), en Markdown y en HTML imprimible.
b) Las piezas de la semana 1 de "70_Contenido/Calendario - primeras 4 semanas.md" (plantilla Pieza de contenido, con
   plataforma, formato, orientacion, embudo y guion), en 70_Contenido/Produccion/.
c) Guion de M0 y de la lección M3.1 del Curso de Nuevos Tutores (plantilla Lección de curso).
d) Plan del Kit del mes 1 de Premium según "50_Cursos/Escalera de productos.md" (solo el plan).

FASE 8 — Verificación final
a) python 99_Sistema/scripts/revisar_boveda.py --salida 00_Inbox/inventario_despues.md y compáralo con
   inventario_antes.md: % de notas con `tipo`, enlaces rotos, carpetas aisladas, huérfanas. Rellena la tabla
   "Números" de la nota de progreso.
b) Ejecuta arbol.py y exportar_flashcards.py (un mazo por nivel en 00_Inbox/).
c) Actualiza Inicio.md si hace falta y escribe la línea final en log.md.
d) Enséñame el resumen antes → después y la rutina semanal para mantenerlo (HANDSHAKE.md §8, paso 7).

Empieza por la FASE 0.
```

---

## 3. Prompt de continuación (para sesiones nuevas)

```text
Continúa la organización de mi segundo cerebro. Lee CLAUDE.md, PLAN_PC.md (el prompt maestro de la sección 2) y
99_Sistema/Organizacion - progreso.md. Dime en qué fase estamos y qué falta, y sigue con la siguiente tarea pendiente
respetando las reglas y los puntos de control ⏸️.
```

---

## 4. Qué esperar

| Fase | Tiempo aprox. | Tu parte |
|---|---|---|
| 0-2 Seguridad, esqueleto y migración | 1 sesión | Aprobar la tabla de destinos |
| 3 Fichas | 1 sesión | — |
| 4 Conectar | **1 sesión por libro** (la más larga) | Aprobar cada fuente |
| 5 Alumnos | 1-2 sesiones | Exportar el CSV, juntar capturas, decir nivel y meta de los antiguos |
| 6 Árbol | 1 sesión | Decidir situaciones nuevas |
| 7-8 Producción y verificación | 1-2 sesiones | Revisar los primeros guiones |

**Señal de éxito:** en el grafo, las "estrellas" de los libros dejan de estar sueltas y quedan unidas por los conceptos
y los nodos del árbol. En el inventario final, ninguna carpeta sale como ⚠️ aislada y los enlaces rotos son 0.

---

## 5. Después: prompts del día a día

| Quiero… | Le digo a Claude |
|---|---|
| Preparar una clase | *"¿Qué hago hoy con Ana?"* · *"Prepara la clase de A2.S05"* |
| Registrar una clase | *"Registra la sesión de Ana: trabajamos… logró…"* (+ capturas) |
| Evaluar | *"Evalúa a Ana: …"* |
| Añadir un libro nuevo | *"Ingiere la fuente 10_Fuentes/Libros/<libro>"* |
| Crear contenido | *"Crea las piezas de la semana 2 del Calendario"* · *"Saca contenido de [[Ser vs estar]]"* |
| Avanzar el curso | *"Prepara la lección M3.2 del curso de tutores"* |
| Premium | *"Prepara el Kit del mes 2 de Premium"* |
| Flashcards | *"Exporta flashcards de A1"* |
| Revisar el sistema | *"Revisa la bóveda: enlaces rotos, carpetas aisladas y notas sin tipo"* |

---

## 6. Si algo sale mal
- **Nada se borra**: lo que sobra está en `90_Archivo/`.
- **Para volver atrás del todo**: cierra Obsidian y restaura el `.zip` de la Fase 0.
- **Enlaces rotos**: *"Ejecuta revisar_boveda.py --enlaces y arregla las rutas"*.
- **Obsidian no muestra los tableros**: activa el plugin núcleo **Bases** (Ajustes → Plugins principales).

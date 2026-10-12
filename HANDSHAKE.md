# 🤝 Handshake v2 — Segundo Cerebro de Español

> El acuerdo entre tú y Claude: **qué construimos, por qué, cómo funciona y cómo ejecutarlo en tu PC**.
> Si algo cambia, se cambia aquí primero y luego en `CLAUDE.md`.

---

## 0. El proyecto en 30 segundos

```
                 ┌──────────────────────── TU CONOCIMIENTO ────────────────────────┐
  10_Fuentes ──▶ 20_Conocimiento (wiki)  ◀── enlaza ──  30_Curriculum/Arbol (100 nodos)
  libros, PDFs,  explicaciones, errores        🟧 situaciones  🟪 gramática  🟩 vocabulario
  capturas       típicos, flashcards              unidos por "requiere" (qué desbloquea qué)
                 └──────────────────────────────────┬──────────────────────────────┘
        ┌───────────────────┬───────────────────────┼──────────────────┬──────────────────┐
        ▼                   ▼                       ▼                  ▼                  ▼
   40_Clases          60_Estudiantes           50_Cursos          70_Contenido       Flashcards
   clases 80/20,      sesiones → ÁRBOL de      ⭐ Tutores (Skool)  redes → Skool      (Anki)
   materiales         cada alumno + métricas   EN (futuro)        gratis → pago
```

**Una frase:** todo tu material vive una sola vez, ordenado en un **árbol de habilidades A0→B2**. De ese
árbol salen tus clases, el progreso visible de cada alumno, tus cursos y tu contenido.

---

## 1. Decisiones tomadas

| Tema | Decisión |
|---|---|
| Producto principal | **Curso de Nuevos Tutores de Español** (nativos que quieren empezar a enseñar) |
| Producto futuro | Cursos ultrasólidos para angloparlantes, A0→B2 |
| Metodología | **Método Misiones 80/20**: mixta, 80 % práctica con situaciones reales (misiones) y **goals medibles**; 20 % input |
| Columna vertebral | **Árbol de habilidades** A0–B2 (sustituye al temario lineal por unidades) |
| Seguimiento de alumnos | Un **árbol por alumno** que se desbloquea con su avance. Sustituye a las capturas sueltas y al Google Sheet |
| Skool | **Dos comunidades**: Skool 1 gratis (dar valor y demostrar el método) → Skool 2 **Premium** de pago |
| Modelo de precio | Según el producto: **curso de introducción = pago único** (incluye 1 mes de Premium); **Premium = suscripción** (asesorías personalizadas, materiales nuevos y actualizados cada mes) |
| Contenido | **Todas las plataformas**, en **vertical y horizontal**: se graba una pieza pilar horizontal y de ella salen clips verticales, carruseles, pins y textos |
| Dónde trabaja Claude | En **tu PC**, directamente sobre la bóveda (Claude Code) |
| Privacidad | Datos de alumnos y libros con copyright **fuera** del repositorio |

---

## 2. Tu metodología, modelada: Método Misiones 80/20

**Situación (misión)** = algo real que el alumno hace + **goals** que se pueden comprobar.

```
A0.S01 Saluda y preséntate
   ⋮
A2.S05 Pregunta por un piso en alquiler        goals: pregunta precio y gastos · compara · concierta visita
   └─▶ B1.S06 Llama al casero por una avería   goals: describe la avería · pide que la arreglen · acuerda fecha
          └─▶ B2.S01 Lee un contrato de alquiler y negocia
                 goals: identifica 3 cláusulas problemáticas · propone alternativas con condicionales · llega a un acuerdo
```

- **Gramática y vocabulario son llaves**: cada situación `requiere` los nodos que necesita (el 20 % de input).
- **Clase 80/20** (plantilla *Plan de clase*): calentamiento → misión y goals → input mínimo → **práctica de la situación** → check de goals.
- **Logrado** = cumple **todos** los goals sin ayuda (4-5 en la escala). Así el progreso es medible y no depende de "me parece que va bien".

---

## 3. El árbol de habilidades

### 3.1 Piezas
| Pieza | Dónde | Qué es |
|---|---|---|
| **Nodo** | `30_Curriculum/Arbol/<Nivel>/` | Una situación (`A1.S07`), una llave de gramática (`A1.G03`) o una de vocabulario (`A1.V03`) |
| **requiere** | propiedad del nodo | Los nodos que hay que dominar antes. Dibujan las flechas |
| **Material** | `40_Clases/Materiales/` | Lectura, ficha, HTML… con `nodos:` → se abre cuando el nodo se desbloquea |
| **Sesión / Evaluación** | `60_Estudiantes/` | `practicados` (trabajados hoy) y `logrados` (goals cumplidos) |

Hoy el árbol tiene **100 nodos** (32 situaciones, 45 de gramática, 23 de vocabulario) y **147 conexiones**.
Es una propuesta inicial: lo ajustas a tu método (fase 3).

### 3.2 Estados de cada nodo para cada alumno (los calcula `arbol.py`)
| Estado | Significa | En su árbol |
|---|---|---|
| ✅ Dominado | Logrado en una sesión/evaluación, o por debajo de su `nivel_base` | Verde |
| 🟡 En curso | Trabajado pero aún no logrado | Ámbar |
| 🔓 Disponible | Todos sus requisitos dominados: **puede hacerlo ya** | Borde azul |
| 🔒 Próximo | Le falta poco: sus requisitos están disponibles o en curso | Gris, discontinuo |
| ⬛ Bloqueado | Aún lejos | **Oculto** (niebla) |

**La niebla** cumple lo que pediste: un alumno A0 **no ve** "Lee una historia corta" (A1). Ve lo que ya
domina, lo que puede hacer ahora y lo que se desbloquea justo después. Con el botón **"Resaltar ruta a la meta"**
aparece su *pathing*: el camino exacto de gramática + vocabulario + situaciones hasta su objetivo.

### 3.3 Ruta y siguiente paso
- Cada alumno tiene una `meta` (p. ej. `B2.S01 Lee un contrato de alquiler y negocia`).
- `arbol.py` calcula **la ruta**: los nodos pendientes en orden, respetando los requisitos.
- **Siguiente paso recomendado**, en este orden: 1) terminar lo que está en curso; 2) lo que está en la ruta a su meta;
  3) el nivel más bajo; 4) situaciones antes que llaves (80 %); 5) lo que más desbloquea.

### 3.4 Cómo se ve
| Vista | Archivo | Para qué |
|---|---|---|
| Árbol del alumno (navegador) | `60_Estudiantes/Arboles/<Alumno>.html` | **Enseñárselo al alumno** (pantalla compartida o enviado) |
| Árbol del alumno (Obsidian) | `60_Estudiantes/Arboles/<Alumno>.canvas` | Tu vista de profe, con enlaces a cada nota |
| Ruta del alumno | `60_Estudiantes/Arboles/<Alumno> - Ruta.md` | Qué puede hacer, qué sigue, qué le falta |
| Panel de todos | `60_Estudiantes/Arboles/Panel de progreso.md` + tablero `Progreso.base` | Alumnos nuevos y antiguos de un vistazo |
| Árbol completo | `30_Curriculum/Arbol maestro.canvas` / `.html` | **Todas las conexiones** entre nodos |

> Ejemplos funcionando con alumnos ficticios: **Demo Emma** (A0, meta: leer historias), **Demo Jake**
> (alumno antiguo con base A1, meta: contrato de alquiler B2) y **Demo Lucía** (antigua, B1).

### 3.5 Medible: métricas por alumno
| Métrica | Qué dice |
|---|---|
| Nivel completado / en curso + % | Dónde está de verdad (un nivel cuenta como completado con el 80 % de sus nodos dominados) |
| Logrados en 30 días | Velocidad de avance |
| Pasos hasta la meta | Cuánto le falta para su objetivo (útil para vender paquetes de clases) |
| Sesiones, última sesión | Constancia. Detecta a quién recuperar |

### 3.6 Optimizable: métricas de tu método (Panel de progreso)
| Métrica | Decisión que te permite tomar |
|---|---|
| **Cuellos de botella**: sesiones de media hasta lograr cada nodo | Mejorar o dividir ese nodo y su material |
| Nodos en curso (cuántos alumnos atascados) | Preparar material o una clase grupal para ese punto |
| Situaciones sin material | Qué material crear primero |

**Ciclo mensual:** revisar el panel → elegir 1 cuello de botella → mejorar su material o dividir el nodo → medir el mes siguiente.

---

## 4. Arquitectura de carpetas

```
00_Inbox/          Captura rápida. Se vacía cada semana.
10_Fuentes/        Material bruto (solo lectura): libros, PDFs, epubs, capturas, CSV del Sheet.
20_Conocimiento/   La wiki: Gramatica · Vocabulario · Funciones · Pronunciacion · Cultura · Pedagogia
30_Curriculum/     🌳 Arbol/<Nivel>/ (100 nodos) · Árbol de habilidades A0-B2 · Arbol maestro · MCER/
40_Clases/         Planes/ (clases 80/20) · Materiales/ (se desbloquean con el árbol)
50_Cursos/         ⭐ Curso_Tutores/ (M0–M9) · Curso_Estudiantes_EN/ (futuro)
60_Estudiantes/    🔒 Alumnos/ · Sesiones/ · Evaluaciones/ · Arboles/ (generado)
70_Contenido/      Ideas/ → Produccion/ → Publicado/ · Lead_magnets/
90_Archivo/        Lo que ya no se usa (aquí está el temario v1 por unidades)
99_Sistema/        Plantillas · Bases (10 tableros) · Taxonomia · scripts
```

---

## 5. Flujos de trabajo

| # | Flujo | Pasos |
|---|---|---|
| A | **Ingerir una fuente** | Ficha *Fuente* → por cada tema, crear o ampliar el concepto en `20_Conocimiento` → enlazarlo a su nodo (`conceptos:`) |
| B | **Preparar una clase** | Elegir la situación (nodo) → *Plan de clase* 80/20 → materiales con `nodos:` |
| C | **Registrar una sesión** (3-5 min) | *Sesión* con `practicados` y `logrados` (+ capturas pegadas dentro) → `python 99_Sistema/scripts/arbol.py` |
| D | **Evaluar** (cada 4-6 clases) | *Evaluación* con `logrados` y escala 1-5 → `arbol.py` |
| E | **Alumno antiguo** | Ficha con `nivel_base` (p. ej. A1) + `dominados` sueltos + `meta` → su árbol aparece ya avanzado |
| F | **Producir contenido** | Situación o concepto → pieza pilar → derivadas por plataforma con `embudo:` |
| G | **Flashcards** | Sección `## Flashcards` (`frente :: reverso`) → `exportar_flashcards.py` → Anki |

### Migración desde tu bóveda actual
| Carpeta actual | Destino |
|---|---|
| `A1Hidalgo…`, `DELE_B2…`, `Lazlo_Sandor…`, `Libros de ESPAÑOL Alfy` | `10_Fuentes/Libros/` |
| `Epubs` | `10_Fuentes/Epubs/` |
| `raw` | `10_Fuentes/` (revisar) |
| `wiki` | `20_Conocimiento/` (reclasificar por área y enlazar a nodos) |
| `MCER` | `30_Curriculum/MCER/` (fusionar) |
| `ideas` | `70_Contenido/Ideas/` o `00_Inbox/` |
| `plantillas`, `scripts` | `99_Sistema/` (fusionar) |
| `CLAUDE`, `index`, `log` | fusionar con `CLAUDE.md`, `Inicio.md`, `log.md` |
| `Untitled`, `Untitled.base` | revisar → borrar o archivar |
| Google Sheet de alumnos | CSV → `10_Fuentes/Sheets/` → fichas (fase 2) |
| Capturas de clases | `10_Fuentes/Capturas_clases/<alumno>/` → sesiones (fase 2) |

---

## 6. Ver TODAS las conexiones en Obsidian

1. **Grafo global** (ya configurado en `.obsidian/graph.json`): colores por tipo, con flechas.
   🟧 situaciones · 🟪 gramática · 🟩 vocabulario · 🔵 conocimiento · 🩵 clases · 🟨 cursos · 🩷 alumnos · 🟢 contenido · ⚪ fuentes.
2. **Grafo local** de cualquier nota: qué la desbloquea y qué desbloquea ella. En la nota *Ruta* de un alumno,
   el grafo local muestra **su** árbol.
3. **Canvas**: `Arbol maestro.canvas` (todo) y `<Alumno>.canvas` (coloreado por su estado). Los nodos son clicables.
4. **Backlinks** de un nodo: qué situaciones lo usan, qué materiales, qué conceptos, qué sesiones.
5. **Bases** (`99_Sistema/Bases/`): tablas filtrables de árbol, alumnos, progreso, sesiones, materiales, contenido y curso.

---

## 7. Oferta y embudo

```
REDES (todas, vertical + horizontal)
   │ lead magnets
   ▼
① COMUNIDAD GRATIS (Skool 1) ──▶ ② CURSO DE INTRODUCCIÓN (pago único) ──▶ ③ PREMIUM (Skool 2, suscripción)
   probar el método                  Curso de Nuevos Tutores M0–M9           asesorías personalizadas, kit mensual
   retos, muestra, directo           + 1 mes de Premium incluido              de materiales nuevos, actualizaciones
```

- **Dar valor primero:** cada semana algo aplicable en la comunidad gratis (reto *Diseña tu situación*, lecciones de muestra,
  directo mensual). La invitación al curso llega al completar 3 retos y al final de cada directo.
- **Premium se ve:** cada mes llega un *Kit del mes* (4 situaciones listas con plan y material), asesorías grupales semanales,
  una asesoría 1:1 y las actualizaciones del sistema. Construir el Premium **es** construir tu bóveda.
- **Contenido:** todas las plataformas. Pilar horizontal 16:9 → 3-5 clips verticales 9:16 → carrusel 4:5 y 1:1 → pins 2:3 → textos.
- Detalle: [[Escalera de productos]] · [[Estrategia de contenido]] · [[Calendario - primeras 4 semanas]] · [[Curso de Nuevos Tutores]].

---

## 8. Plan de ejecución en tu PC (paso a paso)

### Paso 0 — Lo que necesitas instalar
| Herramienta | Para qué |
|---|---|
| **Obsidian** (versión reciente, con Bases) | Tu bóveda |
| **Git** | Descargar el esqueleto y guardar versiones |
| **Python 3.10+** | Ejecutar `arbol.py` y `exportar_flashcards.py` (no necesitan nada más) |
| **Claude Code** (app de escritorio o terminal) | Que Claude trabaje directamente en tu bóveda |

> 🔒 Comprueba que el repositorio `DTAlfy/mi-proyecto` sea **privado** en GitHub.

### Paso 1 — Copia de seguridad
Comprime tu bóveda actual ("Second Brain") en un `.zip` y guárdalo fuera. No se toca hasta que la nueva funcione.

### Paso 2 — Descargar el esqueleto
```bash
git clone https://github.com/DTAlfy/mi-proyecto.git "Segundo Cerebro Español"
cd "Segundo Cerebro Español"
git checkout claude/festive-feynman-6dy8ui     # o main, cuando fusiones esta rama
```

### Paso 3 — Abrirlo en Obsidian
1. Obsidian → *Abrir carpeta como bóveda* → `Segundo Cerebro Español`.
2. Plugins núcleo activados: **Bases, Canvas, Plantillas, Grafo, Propiedades, Backlinks**.
3. Opcionales (comunitarios): **Spaced Repetition** (flashcards dentro de Obsidian) y **Obsidian Git** (copia automática).
4. Abre `Inicio.md`.

### Paso 4 — Comprobar que todo funciona
```bash
python 99_Sistema/scripts/arbol.py --validar     # en Windows: py 99_Sistema\scripts\arbol.py --validar
python 99_Sistema/scripts/arbol.py
```
Abre `60_Estudiantes/Arboles/Demo Emma.html` en el navegador y `30_Curriculum/Arbol maestro.canvas` en Obsidian.

### Paso 5 — Claude toma el control de la bóveda
Abre Claude Code **en la carpeta de la bóveda**. Claude lee `CLAUDE.md` solo y conoce las reglas, carpetas y plantillas.
Claude edita los archivos `.md` directamente y **Obsidian refresca al instante**, sin plugins ni conexiones extra.
También puede ejecutar `arbol.py` por ti después de cada cambio.

### Paso 6 — Ejecutar las fases con Claude (prompts para copiar y pegar)

| Fase | Prompt para Claude Code | Hecho cuando… |
|---|---|---|
| **1. Migrar** | *"Lee HANDSHAKE.md §5. Mi bóveda antigua está en `<ruta>`. Propón el plan de movimiento carpeta por carpeta y espera mi OK antes de mover nada."* | Todo tu material está en su carpeta y `00_Inbox` está vacío |
| **2. Alumnos** | *"Convierte `10_Fuentes/Sheets/alumnos.csv` en fichas con la plantilla Alumno. Para cada alumno antiguo propón `nivel_base` y `meta` y pregúntame lo que no sepas."* · después: *"Con las capturas de `10_Fuentes/Capturas_clases/<alumno>/` crea sus sesiones con practicados y logrados y ejecuta arbol.py."* | Cada alumno (nuevo y antiguo) tiene ficha, árbol y ruta |
| **3. Ajustar el árbol** | *"Revisa `30_Curriculum/Arbol` con mi método 80/20: propón situaciones que falten por nivel, revisa los `requiere` y valida con `arbol.py --validar`."* | El árbol refleja cómo enseñas tú |
| **4. Conectar fuentes** | *"Ingiere la fuente `<libro>`: crea o amplía conceptos en `20_Conocimiento` y enlázalos a sus nodos del árbol."* (un libro por sesión) | El grafo ya no tiene "estrellas" aisladas |
| **5. Materiales** | *"Mira el Panel de progreso y crea materiales para las situaciones que mis alumnos tienen disponibles o en curso."* | Las situaciones activas tienen material |
| **6. Curso de Tutores** | *"Desarrolla el módulo M3 del Curso de Tutores: guion de cada lección con la plantilla Lección de curso."* (módulo a módulo) | M0–M9 con guion listo para grabar |
| **7. Skool + contenido** | *"Crea el lead magnet '10 situaciones listas para tu primera clase' y las piezas de la semana 1 del Calendario."* (semana a semana) | Skool 1 abierto, publicando en todas las plataformas cada semana |
| **7b. Premium** | *"Prepara el Kit del mes 1 de Premium según la Escalera de productos."* (cada mes) | Skool 2 abierto con su primer kit y calendario de asesorías |
| **8. Flashcards** | *"Añade flashcards a los conceptos de A1 y exporta el mazo."* | Mazo por nivel en Anki |

> Las fases 2 a 5 pueden ir en paralelo. Empieza por la **2**: es la que más tiempo te ahorra desde el primer día.

### Paso 7 — Rutina
| Cuándo | Qué | Tiempo |
|---|---|---|
| Después de cada clase | Sesión con `practicados` y `logrados`, o dile a Claude *"registra la sesión de X: …"* | 3-5 min |
| Cada 4-6 clases por alumno | Evaluación | 10 min |
| Semanal | `arbol.py` → revisar el panel · vaciar Inbox · contenido de la semana | 30 min |
| Mensual | Ciclo de optimización (§3.6) · recuperar alumnos antiguos (vista *Antiguos* en Progreso.base) | 1 h |

---

## 9. Fases y criterios de "hecho"

| Fase | Resultado medible |
|---|---|
| 0. Esqueleto ✅ | Este repositorio: árbol, plantillas, tableros, scripts y demos funcionando |
| 1. Migrar | 100 % del material en su carpeta |
| 2. Alumnos | 100 % de alumnos activos con ficha y árbol; antiguos con `nivel_base` |
| 3. Ajustar el árbol | `arbol.py --validar` sin errores y las situaciones revisadas por ti |
| 4. Conectar fuentes | Cada nodo `lista` tiene al menos 1 concepto enlazado |
| 5. Materiales | Menos del 50 % de situaciones sin material (hoy: 31 de 32) |
| 6. Curso de Tutores | 10 módulos con guion; M0 publicado gratis |
| 7. Skool + contenido | 15 piezas por semana (calendario de 4 semanas cumplido) y línea base de métricas anotada |
| 7b. Premium | Skool 2 abierto, primer kit entregado, % del mes incluido → suscripción medido |
| 8. Flashcards | 1 mazo por nivel |
| 9. Curso EN | Tramo A1 publicado |

---

## 10. Decisiones de esta ronda y preguntas abiertas

- [x] Nombre del método → **Método Misiones 80/20**
- [x] Skool → **dos comunidades** (gratis → Premium)
- [x] Modelo → **pago único** para el curso de introducción, **suscripción** para Premium
- [x] Plataformas → **todas**, en vertical y horizontal
- [ ] Precios del curso y de la suscripción
- [ ] Nombres de las dos comunidades (de trabajo: *Tutores 80/20* y *Tutores 80/20 Premium*)
- [ ] ¿Quieres que el alumno reciba su árbol (HTML) por correo después de cada evaluación?

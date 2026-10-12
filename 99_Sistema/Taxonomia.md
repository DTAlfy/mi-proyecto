---
tipo: sistema
---
# Taxonomía — propiedades y valores permitidos

Las **propiedades** (frontmatter) son lo que permite filtrar, medir y generar tableros.
Si un valor no está aquí, **no se usa**. Si hace falta uno nuevo, se añade aquí primero.

## Propiedades comunes a todas las notas

| Propiedad | Valores | Uso |
|---|---|---|
| `tipo` | `concepto` · `fuente` · `nodo` · `material` · `descriptores` · `clase` · `modulo` · `leccion` · `alumno` · `sesion` · `evaluacion` · `ruta` · `idea` · `contenido` · `sistema` | Qué es la nota |
| `estado` | depende del tipo (ver abajo) | En qué punto está |
| `creado` | `AAAA-MM-DD` | Fecha de creación |
| `tags` | libres, en minúscula | Uso puntual; preferir propiedades |

## Niveles (`nivel`)
`A0` · `A1` · `A2` · `B1` · `B2` · `C1` · `tutor`

- `A0` = arranque / pre-A1 (no es un nivel oficial del MCER, pero lo usamos para principiantes absolutos).
- `tutor` = contenido para formar profesores (no es nivel de lengua).

## Conocimiento (`tipo: concepto`)

| Propiedad | Valores |
|---|---|
| `area` | `gramatica` · `vocabulario` · `funcion` · `pronunciacion` · `cultura` · `pedagogia` |
| `nivel` | ver Niveles (puede ser lista: `[A2, B1]`) |
| `destrezas` | `comprension_lectora` · `comprension_auditiva` · `expresion_escrita` · `expresion_oral` · `interaccion` |
| `nodos` | enlaces a nodos del árbol: `["[[A2.G05 Contraste indefinido-imperfecto]]"]` |
| `fuentes` | enlaces a fichas de fuente |
| `usos` | `clase` · `curso_tutores` · `curso_en` · `redes` · `flashcards` |
| `estado` | `borrador` · `revisado` · `listo` |

## Fuentes (`tipo: fuente`)

| Propiedad | Valores |
|---|---|
| `formato` | `libro` · `pdf` · `epub` · `web` · `video` · `podcast` · `sheet` · `capturas` |
| `autor` | texto |
| `nivel` | ver Niveles |
| `estado` | `pendiente` · `procesando` · `procesada` |

## Árbol de habilidades (`tipo: nodo`)

| Propiedad | Valores |
|---|---|
| `codigo` | `<Nivel>.<Rama><nn>` → `A1.S07`, `B1.G04`, `A2.V03` (S = situación, G = gramática, V = vocabulario) |
| `nivel` | ver Niveles |
| `rama` | `situacion` · `gramatica` · `vocabulario` |
| `requiere` | enlaces a los nodos que hay que dominar antes (**solo los directos**) |
| `conceptos` | enlaces a notas de `20_Conocimiento` |
| `estado` | `esqueleto` · `en_desarrollo` · `lista` (estado de la nota, no del alumno) |

Estados que calcula `arbol.py` para cada alumno: `dominado` · `en_curso` · `disponible` · `proximo` · `bloqueado`.

## Materiales (`tipo: material`)

| Propiedad | Valores |
|---|---|
| `formato` | `lectura` · `audio` · `video` · `ficha` · `juego` · `html` · `pdf` · `flashcards` |
| `nivel` | ver Niveles |
| `nodos` | enlaces a los nodos para los que sirve (se desbloquea con ellos) |
| `estado` | `borrador` · `listo` |

## Clases y cursos (`tipo: clase` / `modulo` / `leccion`)

| Propiedad | Valores |
|---|---|
| `curso` | `tutores` · `estudiantes_en` |
| `modulo` | `M0`…`M9` |
| `nodo` | enlace a un nodo del árbol (planes de clase: la situación que trabaja) |
| `duracion_min` | número |
| `formato` | `video` · `texto` · `live` · `ejercicio` · `plantilla` · `pdf` · `html` |
| `estado` | `idea` · `esqueleto` · `guion` · `grabado` · `publicado` |

## Alumnos (`tipo: alumno`)

| Propiedad | Valores |
|---|---|
| `estado` | `prueba` · `activo` · `pausa` · `antiguo` |
| `nivel_base` | nivel ya dominado al empezar (alumnos antiguos o con nivel previo). Vacío = parte de cero |
| `dominados` | enlaces a nodos que ya domina aunque no estén en ninguna sesión |
| `meta` | enlace a la situación objetivo (p. ej. `[[B2.S01 Lee un contrato de alquiler y negocia]]`) |
| `objetivo` | `viaje` · `trabajo` · `examen_dele` · `familia` · `estudios` · `hobby` · `otro` |
| `lengua_materna` | texto |
| `frecuencia` | `1x_semana` · `2x_semana` · `3x_semana` · `irregular` |
| `plataforma_clase` | `zoom` · `meet` · `preply` · `italki` · `skool` · `presencial` · `otra` |
| `inicio` / `proxima_evaluacion` | `AAAA-MM-DD` |

> El nivel y el progreso **no se escriben a mano**: los calcula `arbol.py` en la nota `<Alumno> - Ruta` (`tipo: ruta`).

## Sesiones y evaluaciones (`tipo: sesion` / `evaluacion`)

| Propiedad | Valores |
|---|---|
| `alumno` | enlace a ficha |
| `fecha` | `AAAA-MM-DD` |
| `practicados` | nodos trabajados en la sesión |
| `logrados` | nodos cuyos goals cumplió sin ayuda → pasan a **dominados** |
| `conceptos` | enlaces a conceptos vistos |
| `cl` · `ca` · `ee` · `eo` · `io` | 1–5 por destreza (solo evaluaciones) |
| `resultado` | `mantiene` · `avanza` · `sube_nivel` (solo evaluaciones) |

Escala 1–5: **1** no lo consigue · **2** con mucha ayuda · **3** con algo de ayuda · **4** solo, con errores menores · **5** solo y con soltura.

## Rutas (`tipo: ruta`, generadas por `arbol.py`)
`alumno`, `estado_alumno`, `nivel_completado`, `nivel_en_curso`, `progreso`, `dominados`, `disponibles`,
`logrados_30d`, `sesiones`, `ultima_sesion`, `meta`, `pasos_hasta_meta`, `actualizado`. **No editar a mano.**

## Contenido (`tipo: idea` / `contenido`)

| Propiedad | Valores |
|---|---|
| `audiencia` | `tutores` · `estudiantes_en` · `estudiantes_general` |
| `embudo` | `atraer` (redes) · `captar` (lead magnet / Skool gratis) · `convertir` (pago) · `retener` (alumnos y miembros) |
| `pilar` | `ensenar_espanol` · `negocio_tutor` · `gramatica_facil` · `errores_comunes` · `cultura` · `historias` · `herramientas_ia` |
| `plataforma` | `skool` (comunidad gratis) · `skool_premium` · `instagram` · `tiktok` · `youtube` · `youtube_shorts` · `facebook` · `linkedin` · `threads` · `x` · `newsletter` · `pinterest` |
| `formato` | `reel` · `carrusel` · `post` · `historia` · `video_largo` · `leccion_skool` · `live` · `hilo` · `email` · `pin` · `pdf` · `html` |
| `orientacion` | `horizontal` (16:9) · `vertical` (9:16) · `retrato` (4:5) · `cuadrado` (1:1) · `pin` (2:3) · `texto` |
| `pieza_pilar` | enlace a la pieza larga de la que deriva |
| `origen` | enlace al concepto de `20_Conocimiento` o al nodo (situación) del árbol |
| `estado` | `idea` · `guion` · `produccion` · `programado` · `publicado` · `reciclar` |
| `fecha_publicacion` | `AAAA-MM-DD` |
| `url` | enlace publicado |

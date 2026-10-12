---
tipo: sistema
---
# Taxonomía — propiedades y valores permitidos

Las **propiedades** (frontmatter) son lo que permite filtrar, medir y generar tableros.
Si un valor no está aquí, **no se usa**. Si hace falta uno nuevo, se añade aquí primero.

## Propiedades comunes a todas las notas

| Propiedad | Valores | Uso |
|---|---|---|
| `tipo` | `concepto` · `fuente` · `unidad` · `descriptores` · `clase` · `modulo` · `leccion` · `alumno` · `sesion` · `evaluacion` · `idea` · `contenido` · `sistema` | Qué es la nota |
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
| `unidades` | enlaces a unidades: `["[[A2.05 Contraste indefinido-imperfecto]]"]` |
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

## Curriculum (`tipo: unidad` / `descriptores`)

| Propiedad | Valores |
|---|---|
| `codigo` | `A1.03` |
| `nivel` | ver Niveles |
| `orden` | número |
| `conceptos` | enlaces a notas de `20_Conocimiento` |
| `estado` | `esqueleto` · `en_desarrollo` · `lista` |

## Clases y cursos (`tipo: clase` / `modulo` / `leccion`)

| Propiedad | Valores |
|---|---|
| `curso` | `tutores` · `estudiantes_en` |
| `modulo` | `M0`…`M9` |
| `unidad` | enlace a unidad del roadmap |
| `duracion_min` | número |
| `formato` | `video` · `texto` · `live` · `ejercicio` · `plantilla` · `pdf` · `html` |
| `estado` | `idea` · `esqueleto` · `guion` · `grabado` · `publicado` |

## Alumnos (`tipo: alumno`)

| Propiedad | Valores |
|---|---|
| `estado` | `prueba` · `activo` · `pausa` · `antiguo` |
| `nivel_inicial` / `nivel_actual` / `nivel_objetivo` | ver Niveles |
| `unidad_actual` | enlace a unidad |
| `progreso` | 0–100 (% de descriptores del nivel actual logrados) |
| `objetivo` | `viaje` · `trabajo` · `examen_dele` · `familia` · `estudios` · `hobby` · `otro` |
| `lengua_materna` | texto |
| `frecuencia` | `1x_semana` · `2x_semana` · `3x_semana` · `irregular` |
| `plataforma_clase` | `zoom` · `meet` · `preply` · `italki` · `skool` · `presencial` · `otra` |
| `inicio` / `ultima_sesion` / `proxima_evaluacion` | `AAAA-MM-DD` |

## Sesiones y evaluaciones (`tipo: sesion` / `evaluacion`)

| Propiedad | Valores |
|---|---|
| `alumno` | enlace a ficha |
| `fecha` | `AAAA-MM-DD` |
| `unidad` | enlace a unidad |
| `conceptos` | enlaces a conceptos vistos |
| `cl` · `ca` · `ee` · `eo` · `io` | 1–5 por destreza (solo evaluaciones) |
| `resultado` | `mantiene` · `avanza_unidad` · `sube_nivel` (solo evaluaciones) |

Escala 1–5: **1** no lo consigue · **2** con mucha ayuda · **3** con algo de ayuda · **4** solo, con errores menores · **5** solo y con soltura.

## Contenido (`tipo: idea` / `contenido`)

| Propiedad | Valores |
|---|---|
| `audiencia` | `tutores` · `estudiantes_en` · `estudiantes_general` |
| `pilar` | `ensenar_espanol` · `negocio_tutor` · `gramatica_facil` · `errores_comunes` · `cultura` · `historias` · `herramientas_ia` |
| `plataforma` | `skool` · `instagram` · `tiktok` · `youtube` · `youtube_shorts` · `facebook` · `linkedin` · `threads` · `x` · `newsletter` · `pinterest` |
| `formato` | `reel` · `carrusel` · `post` · `historia` · `video_largo` · `leccion_skool` · `live` · `hilo` · `email` · `pdf` · `html` |
| `pieza_pilar` | enlace a la pieza larga de la que deriva |
| `origen` | enlace al concepto de `20_Conocimiento` |
| `estado` | `idea` · `guion` · `produccion` · `programado` · `publicado` · `reciclar` |
| `fecha_publicacion` | `AAAA-MM-DD` |
| `url` | enlace publicado |

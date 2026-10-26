# Sistema de plantillas (consistencia en todas las diapositivas)

Fuente: `fuentes/02-sistema-de-plantillas-vba.md`, adaptado. El tutorial usa macros VBA porque
una persona edita a mano. Claude genera el archivo con código, así que **la consistencia viene
del script generador** y no hacen falta macros. Se entrega siempre `.pptx` (no `.pptm`).

## Retícula
- Lienzo 16:9 = 13.333" × 7.5" (960 × 540 pt).
- 12 columnas con margen lateral de contenido de 0.8" (el tutorial usa 30 pt; aquí se amplía
  para dar más aire). Zona de contenido: y = 1.85" a 6.45"; pie en 6.9"–7.2".
- `swa.col(n)` y `swa.span(n)` dan coordenadas de la retícula; dos columnas estándar en x = 0.8 y 6.88.

## Tema (colores y fuentes)
- Los colores y fuentes de la marca van en el **tema** de la presentación (ver `assets/guia-de-marca.md`),
  no repetidos como hex en cada forma. Así el usuario puede cambiar la marca en PowerPoint en un solo lugar.
- Fuentes del tema: títulos Georgia, cuerpo Segoe UI. `Clase.guardar()` escribe la paleta y las
  fuentes en el tema; los textos usan las fuentes del tema (`+mj-lt` / `+mn-lt`).

## Tipos de diapositiva
Un tipo por momento de la clase: portada, pregunta, repaso, regla + ejemplos, Compare,
puente EN→ES, truco, "No es lo mismo", texto real, ¡Ojo!, curiosidad, ejercicio,
soluciones, resumen y cierre (ver `pedagogia.md`). `swa.py` dibuja cada diapositiva sobre
el layout en blanco; el pie (ícono, marca y número) lo añade `Clase.diapositiva()` en todas
las diapositivas, con la misma posición y el mismo nombre (así Morph no lo mueve).

## Componentes con nombre
- Nombra (`nombre=`) las formas importantes según su rol (`regla`, `ej0`, `pie_logo`…). Así se ven
  ordenadas en el Panel de Selección de PowerPoint. Las que participan en Morph llevan `!!`
  (ver `tecnicas-visuales.md`).
- Los estilos de cada componente se definen **una vez** como funciones en `scripts/swa.py`
  (`titulo`, `regla`, `ejemplos`, `caja`, `pildora`, `tabla`…). Un componente nuevo se añade allí,
  no se repite en cada clase.

## Animaciones en lote
- (Pendiente en `swa.py`; hoy se usa Morph.) Retardo incremental: cuando varios elementos entran uno tras otro, usar retardos de 0.2 s
  en secuencia (0, 0.2, 0.4…). Nunca más de 4–5 elementos animados por diapositiva.

## Lo que NO se adopta
- Macros VBA, archivos `.pptm`, diapositiva oculta de estilos: no aportan nada cuando se
  genera con código. Solo se escribe VBA si el usuario lo pide expresamente.

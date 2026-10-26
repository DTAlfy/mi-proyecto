# Sistema de plantillas (consistencia en todas las diapositivas)

Fuente: `fuentes/02-sistema-de-plantillas-vba.md`, adaptado. El tutorial usa macros VBA porque
una persona edita a mano. Claude genera el archivo con código, así que **la consistencia viene
del script generador** y no hacen falta macros. Se entrega siempre `.pptx` (no `.pptm`).

## Retícula
- Lienzo 16:9 = 13.333" × 7.5" (960 × 540 pt).
- 12 columnas × 8 filas, márgenes de 30 pt (≈ 0.42") en los cuatro lados.
- Todo elemento se alinea a la retícula: definir en el script `col(n)` y `row(n)` que devuelvan
  coordenadas, y no escribir posiciones "a ojo".

## Tema (colores y fuentes)
- Los colores y fuentes de la marca van en el **tema** de la presentación (ver `marca/guia-de-marca.md`),
  no repetidos como hex en cada forma. Así el usuario puede cambiar la marca en PowerPoint en un solo lugar.
- Fuentes del tema: títulos Georgia, cuerpo Segoe UI.

## Layouts (diseños maestros)
Un layout por tipo de diapositiva de clase: portada, sección, explicación, comparación ES↔EN,
ejemplos, ejercicio, resumen. Pie de página, ícono del logo y número de diapositiva van en el
layout, nunca en cada diapositiva.

## Componentes con nombre
- Cada forma lleva un nombre con prefijo de su rol: `titulo_`, `tarjeta_es_`, `tarjeta_en_`,
  `etiqueta_`, `nota_`, `ejemplo_`. Así se ve ordenado en el Panel de Selección de PowerPoint,
  y además la transición Morph puede emparejar objetos por nombre (ver `tecnicas-visuales.md`).
- Los estilos de cada componente (relleno, radio, tamaño de fuente) se definen **una vez** en el
  script como funciones (`tarjetaEs(slide, texto, x, y)`) y se reutilizan.

## Animaciones en lote
- Retardo incremental: cuando varios elementos entran uno tras otro, usar retardos de 0.2 s
  en secuencia (0, 0.2, 0.4…). Nunca más de 4–5 elementos animados por diapositiva.

## Lo que NO se adopta
- Macros VBA, archivos `.pptm`, diapositiva oculta de estilos: no aportan nada cuando se
  genera con código. Solo se escribe VBA si el usuario lo pide expresamente.

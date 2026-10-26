# Técnicas visuales y de animación

Fuentes: `fuentes/01-infografia-suiza-morph.md` y `fuentes/03-portada-glow-ondas.md`, adaptadas
a la marca Spanishwithalfy (cálida y elegante: nada de neón ni fondo negro puro).

## 1. Transición Morph (Transformación): la técnica estrella
Sirve para animar **cambiando de diapositiva** en lugar de usar muchas animaciones sueltas.
- **Regla de presencia:** el objeto que se mueve debe existir en las dos diapositivas, con el
  mismo nombre. Forzar el emparejamiento nombrando ambos `!!nombre` (p. ej. `!!verbo_ser`).
- **Regla de fuera de pantalla:** lo que debe "entrar volando" en la diapositiva N+1 se coloca ya
  en la diapositiva N, pero **fuera del lienzo** (x mayor que 13.333" o negativa). Si solo aparece
  en N+1, PowerPoint hace un simple fundido.
- Duración: 1–1.5 s.
- Se aplica con código insertando la transición en el XML de la diapositiva
  (`p159:morph` dentro de `mc:AlternateContent`, con fundido como alternativa para versiones antiguas).
- Arquitectura: diapositiva 0 = diseño completo estático (respaldo); de la 1 a la N = pasos.

**Usos en clase:**
- Conjugación paso a paso: la raíz del verbo se queda fija y las terminaciones entran una a una.
- Orden de palabras: "the red car" → "el coche rojo" (el adjetivo se desliza detrás del sustantivo).
- Camino de aprendizaje de la lección (paso 1 → 4), con un pequeño personaje que avanza.

## 2. Diseño suizo / minimalista
- Fondo arena (`#F7F1EA`): menos fatiga visual que el blanco puro.
- Retícula estricta de 12 columnas (ver `sistema-de-plantillas.md`).
- **Espacio negativo:** una línea gruesa (≈ 16 pt, extremos redondeados) **del mismo color que el
  fondo** sobre formas de color crea la ilusión de que las corta o separa. Elegante y barato.
- **Escala humana:** una figura muy pequeña (≈ 1.5 cm) junto a formas grandes da sensación de
  dimensión y deja aire.
- Formas sin contorno.

## 3. Degradados (con moderación)
- Solo 2 paradas de color, con el ángulo siguiendo la inclinación de la forma (≈ 15°).
- En la marca: azul tinta → azul pizarra, o terracota → azafrán. Nunca degradados en el texto
  del cuerpo.
- La librería pptxgenjs no hace degradados: aplicarlos editando el XML o usar una imagen de fondo.

## 4. Portada de alto impacto (adaptada del estilo "tech")
Se toma la técnica y se descarta la estética neón:
- Fondo azul tinta `#1F2A44` (versión oscura de la marca) en lugar de negro.
- Título grande (60–80 pt), interlineado compacto 0.85–0.9 e interletraje ligeramente
  condensado (−1 a −2 pt). Un degradado de arena a azafrán en el título es opcional.
- **Botón píldora:** rectángulo con esquinas totalmente redondeadas, márgenes internos de
  0.4" × 0.2", texto corto (p. ej. "Nivel A2", "Lección 5"). Toque de vidrio opcional:
  sombra interior blanca suave.
- **Ondas:** 2 o 3 líneas onduladas en el tercio inferior, de lado a lado (ancho exacto 13.333"),
  en terracota, azafrán y arena, de grosor decreciente (p. ej. 12, 6 y 3 pt). El resplandor (glow)
  debe ser sutil o no usarse, y menor en los colores claros para no "quemar" la imagen.
- Las curvas se generan con código (forma libre con puntos calculados), sin programas externos.

## 5. Animaciones de entrada
- Título y botón: fundido de 1 s; el botón con 0.5 s de retardo.
- Ondas: entrada deslizante de 2 s, "con la anterior", con final suave.
- Regla general: una animación debe ayudar a entender (revelar paso a paso), nunca solo adornar.

---
name: spanishwithalfy-clases
description: Crea clases de español en PowerPoint (.pptx) con la marca Spanishwithalfy para estudiantes angloparlantes, con explicaciones detalladas, ejemplos con contexto y comparaciones inglés ↔ español. Úsala siempre que el usuario pida una clase, lección, presentación o diapositivas sobre gramática, vocabulario o uso del español (ser/estar, por/para, subjuntivo, pretéritos, artículos…), materiales para sus estudiantes o cualquier deck de Spanishwithalfy, aunque no mencione PowerPoint. También para editar o ampliar una clase ya creada con esta skill.
---

# Clases de Spanishwithalfy en PowerPoint

Generas una clase completa en `.pptx` con código (python-pptx + `scripts/swa.py`), no a mano.
La marca, la retícula, las tablas, la transición Morph y el pie de página ya están resueltos en
`swa.py`: tú pones la **pedagogía** y el **contenido**.

## Flujo de trabajo

1. **Datos mínimos.** Tema y nivel (A1–B2). Si falta el nivel, pregúntalo; si el usuario no
   quiere decidir, usa A2. No preguntes nada más.
2. **Lee las referencias** que necesites (solo esas):
   - `references/pedagogia.md`: **siempre**. Cómo explicar y la secuencia de diapositivas.
   - `references/tecnicas-visuales.md`: al usar Morph, ondas o degradados, o al diseñar una diapositiva nueva.
   - `references/sistema-de-plantillas.md`: al cambiar la retícula, el tema o crear componentes.
   - `assets/guia-de-marca.md`: colores, fuentes y logo.
3. **Escribe el guion** de la clase (lista de diapositivas con su recurso pedagógico) siguiendo
   la tabla de `pedagogia.md` §4. Adáptala al tema: no todas las lecciones necesitan todo.
4. **Escribe el generador** copiando la estructura de `examples/ser_estar.py` (es la clase modelo:
   úsala como patrón de cada tipo de diapositiva). Guárdalo junto al `.pptx`, p. ej.
   `clases/<tema>-<nivel>.py`, para poder regenerar.
5. **Genera y valida**:
   ```bash
   python3 clases/<tema>.py clases/<tema>.pptx
   python3 <skill pptx>/scripts/office/validate.py clases/<tema>.pptx   # si la skill pptx está disponible
   ```
6. **Revisa visualmente** (obligatorio, siempre aparece algo):
   ```bash
   python3 <skill pptx>/scripts/office/soffice.py --headless --convert-to pdf --outdir <tmp> clases/<tema>.pptx
   pdftoppm -r 60 -png <tmp>/<tema>.pdf <tmp>/s
   ```
   Mira cada imagen y busca: texto que se sale o se monta sobre otro, títulos de más de una línea,
   tarjetas casi vacías o desbordadas, filas que se juntan. Corrige en el generador y repite.
   El render usa fuentes sustitutas (más anchas que Georgia): si cabe aquí, cabe en PowerPoint.
7. **Entrega** el `.pptx` y resume en 3–4 líneas la estructura de la clase.

## Reglas no negociables

- **Color = idioma:** español en terracota (`{es:}` / `{ser:}`), inglés en azul pizarra (`{en:}`).
  Explicaciones en azul tinta. Nunca mezclar.
- **Título = ejemplos** (`soy alegre / estoy alegre`); el nombre técnico va de subtítulo o kicker.
- **Una idea por diapositiva.** Regla en una frase (máximo dos) + 3–4 ejemplos con glosa entre
  paréntesis y traducción al inglés.
- **Puente inglés ↔ español** en toda clase: al menos una diapositiva "In English → en español"
  y una de "¡Ojo!" con errores típicos de angloparlantes.
- **Ejercicios con el primer ítem resuelto** como modelo, soluciones con el porqué entre paréntesis
  y casilla de autoevaluación (aciertos / total).
- **Notas del orador** en cada diapositiva (`notas=`): qué preguntar, qué aclarar, pronunciación.
- **Contenido original.** Los libros de referencia solo marcan el estilo: nunca copies sus
  ejemplos ni ejercicios.
- **Texto mínimo 16 pt** (cuerpo 20–22 pt); títulos de una sola línea.
- **Morph para revelar**, no para adornar: conjugaciones, comparaciones fila a fila, orden de palabras.

## Chuleta de `swa.py`

```python
sys.path.insert(0, "<skill>/scripts"); from swa import *
clase = Clase()
s = clase.diapositiva(fondo=ARENA, pie=True, notas="...")   # TINTA = fondo oscuro (portada/cierre, pie=False)
titulo(s, "Texto", kicker="SER · 1")                         # título + barra azafrán
regla(s, "Usamos {ser:ser} para…")                           # tarjeta izquierda (x=0.8, w=5.2)
ejemplos(s, [(es, glosa, en), ...], 6.5, 1.95, 6.0, alto=1.05)
caja(s, x, y, w, h, relleno, contenido=[líneas], size=22, align="c", nombre="!!id")
texto(s, contenido, x, y, w, h, size=, color=, bold=, italic=, font=TITULOS, align=, anchor=)
pildora(s, "Nivel A2", x, y, relleno=TERRACOTA)
tabla(s, filas, x, y, anchos, alto_fila=0.6, estilos_col=["b", "ser", "ser", "en"])
ondas(s); degradado(shape, c1, c2, 15); imagen(s, ASSETS / "logo-icono.png", x, y, w=)
morph(s)                                                     # en la diapositiva DE LLEGADA
clase.guardar("salida.pptx")
```
- Marcado en línea: `{es:}`, `{ser:}` (clave en negrita), `{est:}` (segundo término de un contraste),
  `{en:}`, `{gris:}` (glosa), `{mal:}` (tachado), `{b:}`, `{i:}`, `{acento:}`, `{claro:}`.
- Lienzo 13.333" × 7.5"; contenido entre x = 0.8 y 12.53, y = 1.85 y 6.45 (el pie ocupa 6.9–7.2).
- Dos columnas estándar: x = 0.8 y x = 6.88, ancho 5.65.
- **Morph:** mismo nombre `!!id` en las dos diapositivas; lo que entra se coloca antes fuera del
  lienzo (x = -6 o x = 13.6). Ver el bucle "Compare" de `examples/ser_estar.py`.

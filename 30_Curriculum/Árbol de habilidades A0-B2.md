---
tipo: sistema
---
# 🌳 Árbol de habilidades A0 → B2

La columna vertebral de clases, cursos y seguimiento. Sustituye a un temario lineal:
el alumno **desbloquea** situaciones a medida que domina la gramática y el vocabulario que necesitan.

## Las 3 ramas
| Rama | Código | Qué es | Peso en clase |
|---|---|---|---|
| 🟧 **Situación (misión)** | `A1.S07` | Algo real que el alumno hace, con **goals medibles** | **80 %** |
| 🟪 **Gramática** | `A1.G03` | Una llave que abre situaciones | 20 % |
| 🟩 **Vocabulario** | `A1.V03` | Una llave que abre situaciones | 20 % |

## Cómo funciona
- Cada nodo tiene `requiere:` con los nodos que hay que dominar antes. Eso dibuja las flechas del árbol.
- Un nodo está **disponible** cuando todos sus requisitos están dominados.
- Un alumno **domina** un nodo cuando aparece en `logrados:` de una sesión o evaluación
  (o está por debajo de su `nivel_base`, si es un alumno antiguo).
- Lo que un alumno aún no puede hacer **no se le muestra** (niebla): un A0 no ve "Lee una historia corta" (A1),
  pero sí ve la ruta que lo lleva hasta allí.
- Los **materiales** (`40_Clases/Materiales`) se enlazan a nodos con `nodos:` y solo aparecen cuando el nodo está desbloqueado.

## Ver el árbol
- **Árbol completo:** `Arbol maestro.canvas` (dentro de Obsidian) y `Arbol maestro.html` (navegador).
- **Árbol de cada alumno:** `60_Estudiantes/Arboles/` → se generan con
  `python 99_Sistema/scripts/arbol.py`.
- **Grafo de Obsidian:** colores por rama ya configurados (situaciones naranja, gramática morado, vocabulario verde).
  Abre el *grafo local* de cualquier nodo para ver qué lo desbloquea y qué desbloquea él.

## Añadir o cambiar nodos
1. Crea la nota con la plantilla *Situación (misión)* o *Habilidad (gramática-vocabulario)* en `Arbol/<Nivel>/`.
2. Código: `<Nivel>.<S|G|V><nn>` + título. Ej.: `B1.S08 Organiza una despedida`.
3. Rellena `requiere:` (solo los requisitos **directos**; los indirectos se calculan solos).
4. Ejecuta `python 99_Sistema/scripts/arbol.py --validar` para detectar enlaces rotos o ciclos.

> Tablero: `99_Sistema/Bases/Arbol.base` · Descriptores oficiales de referencia: `MCER/`

## A0

**🟧 Situaciones (misiones)**
- [[A0.S01 Saluda y preséntate]]
- [[A0.S02 Intercambia datos de contacto]]
- [[A0.S03 Sobrevive en clase]]

**🟪 Gramática**
- [[A0.G01 Alfabeto y sonidos]]
- [[A0.G02 Género y número - primera idea]]

**🟩 Vocabulario**
- [[A0.V01 Saludos y despedidas]]
- [[A0.V02 Números del 0 al 100]]
- [[A0.V03 Frases de clase y supervivencia]]

## A1

**🟧 Situaciones (misiones)**
- [[A1.S01 Presenta a tu familia]]
- [[A1.S02 Describe tu casa y tu barrio]]
- [[A1.S03 Cuenta tu rutina diaria]]
- [[A1.S04 Pide en un restaurante]]
- [[A1.S05 Haz planes con un amigo]]
- [[A1.S06 Compra ropa en una tienda]]
- [[A1.S07 Lee una historia corta y cuéntala]]
- [[A1.S08 Escribe un mensaje de presentación]]

**🟪 Gramática**
- [[A1.G01 Ser - identidad, origen y profesión]]
- [[A1.G02 Artículos, género y número]]
- [[A1.G03 Presente regular]]
- [[A1.G04 Estar y hay - ubicación y existencia]]
- [[A1.G05 Presente irregular]]
- [[A1.G06 Verbos reflexivos]]
- [[A1.G07 Gustar y verbos similares]]
- [[A1.G08 Posesivos y demostrativos]]
- [[A1.G09 Ir a + infinitivo]]
- [[A1.G10 Tener que, hay que y poder]]

**🟩 Vocabulario**
- [[A1.V01 Familia y personas]]
- [[A1.V02 Casa, barrio y ciudad]]
- [[A1.V03 Rutina, hora y días]]
- [[A1.V04 Comida y bebida]]
- [[A1.V05 Tiempo libre y gustos]]
- [[A1.V06 Ropa, compras y precios]]

## A2

**🟧 Situaciones (misiones)**
- [[A2.S01 Cuenta tu último viaje]]
- [[A2.S02 Describe tu infancia]]
- [[A2.S03 Ve al médico]]
- [[A2.S04 Resuelve un problema en el hotel]]
- [[A2.S05 Pregunta por un piso en alquiler]]
- [[A2.S06 Explica una receta]]
- [[A2.S07 Lee un relato y cuenta qué pasó]]
- [[A2.S08 Habla de tus planes de futuro]]

**🟪 Gramática**
- [[A2.G01 Pretérito perfecto - experiencias]]
- [[A2.G02 Pretérito indefinido regular]]
- [[A2.G03 Pretérito indefinido irregular]]
- [[A2.G04 Pretérito imperfecto]]
- [[A2.G05 Contraste indefinido-imperfecto]]
- [[A2.G06 Pronombres de objeto directo e indirecto]]
- [[A2.G07 Imperativo afirmativo]]
- [[A2.G08 Comparativos y superlativos]]
- [[A2.G09 Futuro simple]]
- [[A2.G10 Estar + gerundio]]
- [[A2.G11 Por y para - usos básicos]]

**🟩 Vocabulario**
- [[A2.V01 Viajes y transporte]]
- [[A2.V02 Salud y cuerpo]]
- [[A2.V03 Vivienda y anuncios de pisos]]
- [[A2.V04 Trabajo y estudios]]
- [[A2.V05 Carácter y descripción física]]

## B1

**🟧 Situaciones (misiones)**
- [[B1.S01 Entrevista de trabajo]]
- [[B1.S02 Reclama por un servicio]]
- [[B1.S03 Aconseja a un amigo]]
- [[B1.S04 Cuenta una anécdota]]
- [[B1.S05 Opina, acuerda y discrepa]]
- [[B1.S06 Llama al casero por una avería]]
- [[B1.S07 Cuenta lo que te dijeron]]

**🟪 Gramática**
- [[B1.G01 Contraste de los pasados]]
- [[B1.G02 Pluscuamperfecto]]
- [[B1.G03 Presente de subjuntivo - formas]]
- [[B1.G04 Subjuntivo - deseos, peticiones y consejos]]
- [[B1.G05 Subjuntivo - valoración y sentimientos]]
- [[B1.G06 Imperativo negativo y con pronombres]]
- [[B1.G07 Condicional simple]]
- [[B1.G08 Estilo indirecto]]
- [[B1.G09 Oraciones de relativo]]
- [[B1.G10 Ser y estar - usos avanzados]]
- [[B1.G11 Conectores y argumentación]]

**🟩 Vocabulario**
- [[B1.V01 Trabajo y entrevistas]]
- [[B1.V02 Vivienda - contratos, gastos y averías]]
- [[B1.V03 Sentimientos y relaciones]]
- [[B1.V04 Medios, noticias y opinión]]
- [[B1.V05 Quejas y reclamaciones]]

## B2

**🟧 Situaciones (misiones)**
- [[B2.S01 Lee un contrato de alquiler y negocia]]
- [[B2.S02 Debate un tema de actualidad]]
- [[B2.S03 Escribe una reclamación formal]]
- [[B2.S04 Negocia condiciones laborales]]
- [[B2.S05 Media en un conflicto entre vecinos]]
- [[B2.S06 Simulacro DELE B2]]

**🟪 Gramática**
- [[B2.G01 Imperfecto de subjuntivo]]
- [[B2.G02 Oraciones condicionales]]
- [[B2.G03 Subjuntivo en oraciones temporales]]
- [[B2.G04 Subjuntivo en concesivas y finales]]
- [[B2.G05 Perfecto y pluscuamperfecto de subjuntivo]]
- [[B2.G06 Correlación de tiempos]]
- [[B2.G07 Voz pasiva y pasiva refleja]]
- [[B2.G08 Perífrasis verbales avanzadas]]
- [[B2.G09 Estilo indirecto completo]]
- [[B2.G10 Marcadores discursivos]]
- [[B2.G11 Registro formal e informal]]

**🟩 Vocabulario**
- [[B2.V01 Lenguaje jurídico y contratos]]
- [[B2.V02 Economía y mundo laboral]]
- [[B2.V03 Sociedad y temas de debate]]
- [[B2.V04 Expresiones idiomáticas]]

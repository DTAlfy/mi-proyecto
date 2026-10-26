"""Clase modelo: soy alegre / estoy alegre (ser y estar), nivel A2.

Ejemplo de referencia de la skill: muestra la secuencia pedagógica completa y el uso de swa.py.
Uso: python3 ser_estar.py salida.pptx
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from swa import *  # noqa: E402,F403

clase = Clase()

# 1. Portada -------------------------------------------------------------------------
s = clase.diapositiva(TINTA, pie=False, notas=(
    "Presenta el tema con los dos ejemplos del título. Pregunta: Do you know why Spanish "
    "needs two verbs here? No des la respuesta todavía."))
imagen(s, ASSETS / "logo-icono-claro.png", M, 0.6, w=0.55, nombre="!!logo")
texto(s, "Spanish {acento:with alfy}", M + 0.7, 0.62, 5, 0.5, size=20, color=ARENA,
      bold=True, font=TITULOS, anchor="m")
texto(s, "soy alegre {gris:/} {acento:estoy alegre}", M, 2.0, 11.7, 1.3, size=52, color=ARENA,
      bold=True, font=TITULOS, align="c", nombre="!!portada_titulo", interlineado=0.9)
texto(s, "Ser y estar: cuándo usar cada uno", M, 3.35, 11.7, 0.6, size=26, color=ARENA,
      align="c", nombre="!!portada_sub")
pildora(s, "Nivel A2", W / 2 - 0.9, 4.3, w=1.8, nombre="!!pildora")
ondas(s)

# 2–3. Pregunta curiosa (Morph: «to be» se divide en dos verbos) -------------------------
notas_pregunta = (
    "En inglés hay un solo verbo, to be. En español hay dos. Deja que los estudiantes "
    "adivinen la diferencia antes de seguir.")
for paso in (0, 1):
    s = clase.diapositiva(notas=notas_pregunta)
    if paso:
        morph(s)
    texto(s, "In English, one verb:", M if paso else 3.67, 1.4, 6, 0.5, size=18, color=EN,
          nombre="!!kick_en", align="l" if paso else "c")
    texto(s, "to be", M if paso else 3.67, 1.9, 6, 1.3, size=64, color=EN, italic=True,
          font=TITULOS, nombre="!!tobe", align="l" if paso else "c")
    texto(s, "En español, dos verbos:", 6.6 if paso else 14, 1.4, 5.6, 0.5, size=18, color=ES,
          nombre="!!kick_es")
    texto(s, "ser · estar", 6.6 if paso else 14, 1.9, 6.2, 1.3, size=60, color=ES, bold=True,
          font=TITULOS, nombre="!!serestar")
    texto(s, "¿Por qué decimos «{ser:soy} profesora» pero «{ser:estoy} cansada»?",
          M, 4.4 if paso else 8, 11.7, 1, size=30, color=TINTA, italic=True, font=TITULOS,
          align="c", nombre="!!pregunta")

# 4. Repasa ------------------------------------------------------------------------------
s = clase.diapositiva(notas=(
    "Repaso rápido. Señala las tildes: estás, está, están. Pronunciación: el acento va en "
    "la última sílaba (es-TÁS)."))
titulo(s, "Presente de ser y estar", kicker="▶ Repasa")
tabla(s, [["", "SER", "ESTAR", "English"],
          ["yo", "soy", "estoy", "I am"],
          ["tú", "eres", "estás", "you are"],
          ["él, ella, usted", "es", "está", "he / she is, you are"],
          ["nosotros, nosotras", "somos", "estamos", "we are"],
          ["vosotros, vosotras", "sois", "estáis", "you are (Spain)"],
          ["ellos, ellas, ustedes", "son", "están", "they are, you are"]],
      M, 1.85, [3.4, 2.6, 2.6, 3.1], alto_fila=0.6, size=18,
      estilos_col=["b", "ser", "ser", "en"])

# 5–8. Reglas -----------------------------------------------------------------------------
reglas = [
    ("SER · 1", "Ser: cómo es alguien o algo",
     "Usamos {ser:ser} para las características {b:normales} o {b:permanentes}: personalidad, "
     "aspecto, origen, profesión, material.",
     [("María {ser:es} muy activa.", "(Es así normalmente.)", "María is very active."),
      ("{ser:Soy} de Colombia.", "(Origen.)", "I'm from Colombia."),
      ("Mi hermano {ser:es} médico.", "(Profesión.)", "My brother is a doctor."),
      ("La mesa {ser:es} de madera.", "(Material.)", "The table is made of wood.")],
     "Ser responde a la pregunta «¿cómo es?». Pide a cada estudiante una frase sobre su familia."),
    ("SER · 2", "Ser: dónde y cuándo es un evento",
     "Con {b:eventos} (fiesta, clase, concierto, boda) usamos {ser:ser} para decir "
     "{b:dónde} y {b:cuándo} ocurren.",
     [("La fiesta {ser:es} en mi casa.", "(Evento → lugar.)", "The party is at my house."),
      ("La clase {ser:es} a las diez.", "(Hora.)", "The class is at ten."),
      ("El concierto {ser:es} el sábado.", "(Día.)", "The concert is on Saturday."),
      ("Hoy {ser:es} lunes.", "(Fecha.)", "Today is Monday.")],
     "Es la regla que más sorprende: un evento «es» en un lugar. Compárala luego con estar + lugar."),
    ("ESTAR · 1", "Estar: cómo está alguien o algo ahora",
     "Usamos {ser:estar} para {b:estados temporales}, emociones y cambios: cómo estás hoy, "
     "no cómo eres.",
     [("Hoy {ser:estoy} cansada.", "(Solo hoy.)", "I'm tired today."),
      ("Este café {ser:está} frío.", "(Ahora, no siempre.)", "This coffee is cold."),
      ("¡Qué guapo {ser:estás} con esa camisa!", "(Hoy, con esa ropa.)", "You look great in that shirt!"),
      ("{ser:Estamos} muy contentos.", "(Emoción.)", "We're very happy.")],
     "Estar responde a «¿cómo está?». Truco: si en inglés puedes decir «right now», suele ser estar."),
    ("ESTAR · 2", "Estar: dónde está alguien o algo",
     "Para la {b:ubicación} de personas, cosas y lugares usamos {ser:estar}.",
     [("Madrid {ser:está} en el centro de España.", "", "Madrid is in the centre of Spain."),
      ("¿Dónde {ser:están} mis gafas?", "", "Where are my glasses?"),
      ("{ser:Estoy} en casa.", "", "I'm at home."),
      ("El banco {ser:está} al lado del parque.", "", "The bank is next to the park.")],
     "Contrasta con la diapositiva de eventos: la fiesta ES en casa, pero la casa ESTÁ en Madrid."),
]
for kicker, tit, txt_regla, items, notas in reglas:
    s = clase.diapositiva(notas=notas)
    titulo(s, tit, kicker=kicker)
    regla(s, txt_regla)
    ejemplos(s, items, 6.5, 1.95, 6.0, alto=1.05)

# 9–12. Compare (Morph: las filas entran una a una) ------------------------------------
pares = [
    ("Julián {ser:es} alegre.", "(Es así normalmente.)",
     "Julián {ser:está} alegre.", "(Hoy, por algo especial.)"),
    ("El hielo {ser:es} frío.", "(Siempre.)",
     "Este café {ser:está} frío.", "(Ahora.)"),
    ("La boda {ser:es} en la iglesia.", "(Evento.)",
     "La iglesia {ser:está} en la plaza.", "(Lugar físico.)"),
]
for paso in range(len(pares) + 1):
    s = clase.diapositiva(notas=(
        "Avanza fila por fila. Antes de cada clic, pide que adivinen la explicación."))
    if paso:
        morph(s)
    titulo(s, "Compare:", kicker="Ser y estar")
    caja(s, M, 1.85, 5.65, 0.6, TERRACOTA, contenido="SER", size=20, color=BLANCO, bold=True,
         align="c", nombre="!!cab_ser", espacio=0)
    caja(s, 6.88, 1.85, 5.65, 0.6, TINTA, contenido="ESTAR", size=20, color=BLANCO, bold=True,
         align="c", nombre="!!cab_est", espacio=0)
    for n, (a, ga, b, gb) in enumerate(pares):
        dentro = n < paso
        y = 2.65 + n * 1.25
        caja(s, M if dentro else -6, y, 5.65, 1.05, contenido=[a, f"{{gris:{ga}}}"], size=22,
             color=ES, nombre=f"!!c{n}_ser", espacio=0.05)
        caja(s, 6.88 if dentro else 13.6, y, 5.65, 1.05, contenido=[b, f"{{gris:{gb}}}"], size=22,
             color=ES, nombre=f"!!c{n}_est", espacio=0.05)

# 13. In English → en español ------------------------------------------------------------
s = clase.diapositiva(notas=(
    "Lee la frase en inglés y pide la traducción antes de mostrarla. La etiqueta indica qué "
    "regla se aplica."))
titulo(s, "In English → en español", kicker="El puente")
filas = [("I am tall.", "Soy alto.", "SER"),
         ("I am tired.", "Estoy cansado.", "ESTAR"),
         ("The party is at Ana's house.", "La fiesta es en casa de Ana.", "SER"),
         ("Ana's house is in Madrid.", "La casa de Ana está en Madrid.", "ESTAR"),
         ("The soup is cold.", "La sopa está fría.", "ESTAR")]
for n, (en, es, verbo) in enumerate(filas):
    y = 1.9 + n * 0.74
    texto(s, f"{{en:{en}}}", M, y, 4.5, 0.6, size=21, anchor="m")
    texto(s, "→", 5.3, y, 0.6, 0.6, size=21, color=GRIS, anchor="m", align="c")
    texto(s, f"{{es:{es}}}", 5.95, y, 5.0, 0.6, size=21, anchor="m")
    pildora(s, verbo, 11.25, y + 0.08, relleno=TERRACOTA if verbo == "SER" else TINTA, size=13, w=1.25)
texto(s, "Un verbo en inglés, dos en español. La pregunta clave: {ser:¿cómo es?} o {ser:¿cómo está?}",
      M, 5.75, 11.7, 0.6, size=20, color=TINTA, italic=True, font=TITULOS, align="c")

# 14. Truco mental -------------------------------------------------------------------------
s = clase.diapositiva(notas=(
    "Mnemotecnia muy usada con angloparlantes. Aclara que es una ayuda, no una regla perfecta "
    "(ver la curiosidad de «está muerto»)."))
titulo(s, "Un truco para recordar: DOCTOR y PLACE", kicker="Truco mental")
doctor = [("D", "Description", "Es alto."), ("O", "Occupation", "Es profesora."),
          ("C", "Characteristic", "Es simpático."), ("T", "Time", "Son las tres."),
          ("O", "Origin", "Soy de Perú."), ("R", "Relationship", "Es mi hermana.")]
place = [("P", "Position", "Está sentado."), ("L", "Location", "Está en casa."),
         ("A", "Action (-ndo)", "Estoy comiendo."), ("C", "Condition", "Está enfermo."),
         ("E", "Emotion", "Estoy feliz.")]
for x, cab, color, lista in ((M, "SER = DOCTOR", TERRACOTA, doctor),
                             (6.88, "ESTAR = PLACE", TINTA, place)):
    caja(s, x, 1.85, 5.65, 4.55, BLANCO)
    texto(s, cab, x + 0.35, 2.0, 5, 0.5, size=20, color=color, bold=True, font=TITULOS)
    texto(s, [f"{{b:{l}}}  {{en:{w}}}  {{es:{e}}}" for l, w, e in lista], x + 0.35, 2.6, 5.1, 3.7,
          size=20, espacio=0.6)

# 15. No es lo mismo ----------------------------------------------------------------------------
s = clase.diapositiva(notas=(
    "Aburrido es el mejor ejemplo para angloparlantes: boring / bored. Practica con mímica."))
titulo(s, "No es lo mismo…", kicker="Cambian de significado")
for n, (a, ea, b, eb) in enumerate([
        ("ser aburrido", "boring", "estar aburrido", "bored"),
        ("ser listo", "clever", "estar listo", "ready"),
        ("ser malo", "bad (person, product)", "estar malo", "sick"),
        ("ser rico", "rich", "estar rico", "tasty")]):
    y = 1.85 + n * 1.12
    caja(s, M, y, 5.65, 0.95, contenido=f"{{ser:{a}}}  =  {{en:{ea}}}", size=22, nombre=f"nm{n}a")
    caja(s, 6.88, y, 5.65, 0.95, contenido=f"{{ser:{b}}}  =  {{en:{eb}}}", size=22, nombre=f"nm{n}b")

# 16. Texto real anotado ---------------------------------------------------------------------------
s = clase.diapositiva(notas=(
    "Lectura en voz alta. Después, los estudiantes explican cada verbo con DOCTOR / PLACE."))
titulo(s, "Lee y observa", kicker="Texto real")
caja(s, M, 1.85, 11.7, 3.45, contenido=(
    "¡Hola! Me llamo Lucía. {ser:Soy} de Sevilla, pero ahora {est:estoy} en Londres. "
    "{ser:Soy} profesora de español y {est:estoy} muy contenta con mi trabajo. Hoy {ser:es} lunes "
    "y {est:estoy} un poco cansada. Mi clase {ser:es} a las diez y el aula {est:está} en el segundo "
    "piso. Mis estudiantes {ser:son} muy simpáticos… ¡y hoy {est:están} nerviosos porque {ser:es} "
    "día de examen!"), size=22, padding=0.45, interlineado=1.3)
texto(s, "{ser:soy, es, son} = ser      {est:estoy, está, están} = estar", M, 5.45, 11.7, 0.4,
      size=16, align="c")
texto(s, "¿Por qué Lucía {ser:es} profesora pero {est:está} contenta?", M, 5.95, 11.7, 0.5,
      size=22, italic=True, font=TITULOS, align="c")

# 17. ¡Ojo! ---------------------------------------------------------------------------------------
s = clase.diapositiva(notas=(
    "Errores reales de estudiantes angloparlantes. Pide que expliquen la corrección en inglés."))
titulo(s, "¡Ojo! Errores típicos", kicker="Para angloparlantes")
for n, (mal, bien, porque) in enumerate([
        ("Soy cansado.", "Estoy cansado.", "A temporary state, not who you are."),
        ("Estoy profesor.", "Soy profesor.", "Occupation → ser."),
        ("La fiesta está en mi casa.", "La fiesta es en mi casa.", "Location of an event → ser."),
        ("Madrid es en España.", "Madrid está en España.", "Location of a place → estar.")]):
    y = 1.85 + n * 1.12
    caja(s, M, y, 11.7, 0.95, BLANCO)
    texto(s, f"✗  {{mal:{mal}}}", M + 0.35, y, 4.6, 0.95, size=19, color=GRIS, anchor="m")
    texto(s, f"✓  {{ser:{bien}}}", 5.35, y, 4.0, 0.95, size=19, color=TINTA, anchor="m")
    texto(s, f"{{en:{porque}}}", 9.4, y, 2.9, 0.95, size=14, anchor="m")

# 18. Curiosidad -------------------------------------------------------------------------------------
s = clase.diapositiva(notas=(
    "La muerte es permanente, pero se usa estar: estar expresa el resultado de un cambio "
    "(vivo → muerto). Por eso «permanente = ser» es solo una ayuda."))
titulo(s, "¿Permanente = ser? No siempre", kicker="Curiosidad")
pildora(s, "Curiosidad", M, 2.05, relleno=AZAFRAN, color=TINTA, size=14)
texto(s, "La muerte es para siempre… pero decimos\n{ser:Esta planta está muerta.}   {mal:Esta planta es muerta.}",
      M, 2.75, 11.7, 1.6, size=30, font=TITULOS, interlineado=1.2)
texto(s, "{ser:Estar} describe el {b:resultado de un cambio} (viva → muerta), aunque ese estado ya no "
      "cambie.\n{en:That's why “permanent = ser” is a helpful rule of thumb, not a perfect rule.}",
      M, 4.45, 11.7, 1.6, size=20)

# 19–20. Ejercicios (primer ítem resuelto, como modelo) -------------------------------------------
ej1 = ["Yo (soy / estoy) estudiante de español.",
       "Hoy mis padres (son / están) en Barcelona.",
       "La clase de yoga (es / está) en el gimnasio.",
       "¡Esta sopa (es / está) muy rica!",
       "Mi novia (es / está) de México.",
       "¿Por qué (eres / estás) triste?",
       "El examen (es / está) el jueves.",
       "Las llaves (son / están) en la mesa."]
ej2 = ["Mi hermano ____ muy alto.",
       "¿Dónde ____ (tú)? Te estoy esperando.",
       "Nosotros ____ ingleses, pero vivimos en Valencia.",
       "La película ____ aburrida: me voy a dormir.",
       "Los niños ____ aburridos porque llueve.",
       "¿____ lista? ¡Nos vamos!",
       "Ya ____ las ocho.",
       "El café ____ frío, ¿lo caliento?"]
for num, tit, items, modelo in ((1, "Rodee la forma correcta", ej1, "soy"),
                                (2, "Complete con ser o estar", ej2, "es")):
    s = clase.diapositiva(notas="El primer ítem está resuelto como modelo. 5 minutos.")
    titulo(s, tit, kicker=f"Ejercicio {num}")
    lineas = [f"{{b:1.}}  {items[0]}   →  {{ser:{modelo}}}"]
    lineas += [f"{{b:{i}.}}  {t}" for i, t in enumerate(items[1:], start=2)]
    caja(s, M, 1.85, 11.7, 4.55, contenido=lineas, size=21, padding=0.45, espacio=0.38, anchor="t")

# 21. Soluciones y autoevaluación --------------------------------------------------------------------
s = clase.diapositiva(notas="Corrijan juntos. Si hay errores, vuelvan a la regla que lo explica.")
titulo(s, "Soluciones", kicker="Autoevaluación")
sol1 = ["2. están (lugar)", "3. es (evento)", "4. está (sabor ahora)", "5. es (origen)",
        "6. estás (emoción)", "7. es (evento → cuándo)", "8. están (lugar)"]
sol2 = ["2. estás (lugar)", "3. somos (origen)", "4. es (boring)", "5. están (bored)",
        "6. Estás (= preparada)", "7. son (hora)", "8. está (ahora)"]
for x, cab, sol in ((M, "Ejercicio 1", sol1), (6.88, "Ejercicio 2", sol2)):
    texto(s, cab, x, 1.85, 5.6, 0.45, size=20, bold=True, font=TITULOS)
    texto(s, sol, x, 2.35, 5.6, 3.4, size=18, espacio=0.3)
caja(s, M, 5.85, 11.7, 0.6, AZAFRAN, contenido="Mis aciertos:  ____ / 14", size=20, bold=True,
     align="c", espacio=0)

# 22. Resumen -----------------------------------------------------------------------------------------
s = clase.diapositiva(notas="Resumen final para fotografiar o descargar.")
titulo(s, "Resumen", kicker="Ser y estar")
tabla(s, [["¿Qué expresa?", "SER", "ESTAR"],
          ["Características", "normales: Es alegre.", "temporales: Está alegre."],
          ["Lugar", "de un evento: La fiesta es aquí.", "de personas y cosas: Está aquí."],
          ["Tiempo", "hora y fecha: Son las tres.", "—"],
          ["Profesión, origen", "Es médica. Es de Perú.", "—"],
          ["Emociones, estados", "—", "Está cansada. Está muerta."],
          ["Truco", "DOCTOR", "PLACE"]],
      M, 1.85, [3.1, 4.3, 4.3], alto_fila=0.6, size=17, estilos_col=["b", "es", "es"])

# 23. Cierre ---------------------------------------------------------------------------------------------
s = clase.diapositiva(TINTA, pie=False, notas="Despedida. Tarea: escribir 5 frases sobre tu día con ser y estar.")
imagen(s, ASSETS / "logo-icono-claro.png", W / 2 - 0.5, 1.6, w=1.0, nombre="!!logo")
texto(s, "¡Hasta la próxima!", M, 2.85, 11.7, 1.0, size=54, color=ARENA, bold=True, font=TITULOS,
      align="c", nombre="!!portada_titulo")
texto(s, "Tarea: escribe 5 frases sobre tu día con {acento:ser} y {acento:estar}.", M, 3.95, 11.7,
      0.6, size=22, color=ARENA, align="c", nombre="!!portada_sub")
ondas(s)

print(clase.guardar(sys.argv[1] if len(sys.argv) > 1 else "ser-estar.pptx"))

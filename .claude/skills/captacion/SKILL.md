---
name: captacion
description: Contenido de marketing del curso (Shorts/Reels, lead magnet, página de ventas, upsell) alineado con el currículo.
disable-model-invocation: true
argument-hint: "shorts|lead-magnet|ventas|upsell"
---

# /captacion $ARGUMENTS

Contexto: `python builder.py contexto 1` (o el módulo que toque). Salida en `06_Marketing/`, un archivo por pieza.
- Shorts/Reels (`shorts/S[NNN]_[Clave].md`): de 30 a 45 s, gancho en 2 s, "antes y después" de un tutor, un único CTA al mini-curso gratis. Puede usar `[BROLL]`/`[SLIDE]`.
- Lead magnet: mini-curso de 3 lecciones sacado del Módulo 1, que termina en la oferta.
- Página de ventas: promesa, para quién es y para quién no, temario, garantía, preguntas frecuentes y CTA (`config.yaml › proyecto.enlaces`).
- Upsell: auditoría de perfil 1 a 1 (TidyCal).
Sin testimonios ni cifras inventadas (`[NOTA: testimonio real]`). Sin prometer ingresos.

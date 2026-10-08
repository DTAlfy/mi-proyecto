---
name: preparar-grabacion
description: Deja lista una lección para grabar (assets visuales, teleprompter y checklist). Úsala cuando Alfy diga "prepara M01 L01", "quiero grabar mañana el módulo 2" o "genera los visuales".
---

# Skill: Kit de grabación

Argumentos: `MM LL` o `MM` (módulo completo).

1. `python builder.py validar MM LL`. Si hay errores, arréglalos en el guion primero.
2. `python builder.py preparar MM LL` (dry-run): genera gratis slides, roadmap, teleprompter y checklist, y lista las llamadas de pago.
3. Muestra a Alfy una tabla con lo que costaría (llamadas por proveedor y coste estimado) y **pregunta si genera**. No sigas sin un "sí" explícito.
4. Con confirmación: `python builder.py preparar MM LL --generar`. Si el tope de presupuesto lo bloquea, informa y pregunta antes de usar `--forzar-presupuesto`.
5. Abre `01_Guiones/teleprompter/M.._CHECKLIST.md` y resume qué tiene que tener abierto en pantalla al grabar (las indicaciones `[PANTALLA]`).
6. Si algún asset generado no encaja, cambia solo el prompt de esa etiqueta en el guion y regenera. La caché evita pagar de nuevo los demás.

---
name: workbook
description: Genera o mejora el workbook PDF de un módulo a partir de los bloques [TAREA] y [RECURSO] de sus guiones. Úsala cuando Alfy pida "el workbook del módulo 2" o "materiales de apoyo".
---

# Skill: Workbooks

1. Lee los guiones del módulo `MM` y revisa que cada lección tenga al menos un `[TAREA]` y un `[RECURSO]`. Si faltan o son flojos, propón y escribe mejoras en el guion (no en el HTML generado).
2. Las capturas (Lightshot o Flameshot) se guardan como `03_Assets_Generados/CAPTURAS/M[MM]_L[LL]_descripcion.png` y se añaden solas a su lección.
3. `python builder.py workbook MM` → `04_Workbooks/M[MM]_Workbook.pdf` (usa Edge o Chrome en modo headless; `--solo-html` si no hay navegador).
4. Comprueba que los enlaces de `config.yaml › proyecto.enlaces` (Skool, TidyCal) no sean los de ejemplo antes de publicar.

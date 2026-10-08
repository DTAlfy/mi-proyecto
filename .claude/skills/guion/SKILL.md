---
name: guion
description: Escribe o reescribe el guion de una lección del curso (o de todas las lecciones de un módulo) siguiendo la estructura pedagógica y las etiquetas del pipeline. Úsala cuando Alfy pida "guion de M01 L02", "escribe el módulo 3" o "mejora este guion".
---

# Skill: Generador de guiones

Argumentos: `MM LL` (una lección) o `MM` (todas las lecciones del módulo que aún no tengan guion).

## Pasos
1. Lee `00_Sistema/curriculum.yaml` (título, objetivo, módulo, hito y lecciones vecinas) y `docs/FORMATO_GUION.md`.
2. Si existe, lee el guion de la lección anterior para encadenar el cierre con la apertura. Si no hay guion, crea el esqueleto con `python builder.py nuevo MM LL`.
3. Escribe el guion completo en `01_Guiones/M[MM]_L[LL]_[Clave].md` respetando:
   - Frontmatter con `leccion`, `clave`, `titulo`, `modulo`, `objetivo`, `duracion_objetivo_min` y `estado: borrador`.
   - Estructura: Hook (15 s, un problema crítico) → `[ROADMAP]` (dónde estamos) → Problema → Solución (método en pasos) → Demostración con `[PANTALLA: ...]` → `[TAREA]` + `[RECURSO]` → Cierre con un puente a la siguiente lección.
   - Entre 1.100 y 1.300 palabras leídas para 8 min (unas 150 palabras por minuto).
   - Un visual cada 20 o 30 segundos de lectura: `[BROLL]` para emoción o contexto, `[SLIDE]` para listas o fórmulas, `[IMG]` para metáforas. Como máximo 3 `[BROLL]` por lección (son lo más caro).
   - Prompts visuales en inglés, de 3 a 6 palabras, concretos (sujeto + acción + lugar), sin texto ni marcas.
   - `[TAREA]` accionable en menos de 30 min, con plantilla o tabla para rellenar. `[RECURSO]` con ejemplos o plantillas listas.
   - Ningún dato inventado: `[NOTA: verificar ...]` cuando haga falta una cifra.
4. Ejecuta `python builder.py validar MM LL` y corrige hasta que no haya errores (los avisos de duración también cuentan).
5. Resume para Alfy: duración estimada, número de visuales por tipo y llamadas de pago que generará (ejecuta `python builder.py assets MM LL`, que es un dry-run).

Para un módulo completo, repite los pasos por lección en orden y valida cada una antes de seguir.

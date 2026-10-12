---
tipo: sistema
---
# 🧠 Segundo Cerebro de Español — Inicio

## 🌳 El árbol
- [[Árbol de habilidades A0-B2]] — la columna vertebral (situaciones 80 % + gramática y vocabulario 20 %)
- [[30_Curriculum/Arbol maestro.canvas|Árbol maestro (Canvas)]] — todas las conexiones
- [[Panel de progreso]] — todos tus alumnos y los cuellos de botella *(se genera con `arbol.py`)*

## Tableros
| Tablero | Para qué |
|---|---|
| [[99_Sistema/Bases/Progreso.base\|📈 Progreso]] | Nivel, % y ruta de cada alumno (calculado) |
| [[99_Sistema/Bases/Alumnos.base\|👩‍🎓 Alumnos]] | Fichas: activos, antiguos, metas |
| [[99_Sistema/Bases/Sesiones.base\|🗓️ Sesiones]] | Historial de clases (practicados / logrados) |
| [[99_Sistema/Bases/Evaluaciones.base\|📝 Evaluaciones]] | Evolución por destreza |
| [[99_Sistema/Bases/Arbol.base\|🌳 Árbol]] | Nodos por nivel, situaciones, qué falta desarrollar |
| [[99_Sistema/Bases/Materiales.base\|📦 Materiales]] | Materiales por nivel y nodo |
| [[99_Sistema/Bases/Conocimiento.base\|📚 Conocimiento]] | La wiki por nivel y área |
| [[99_Sistema/Bases/Cursos.base\|🎓 Cursos]] | Avance del Curso de Tutores |
| [[99_Sistema/Bases/Contenido.base\|📣 Contenido]] | Pipeline de redes y Skool (con embudo) |
| [[99_Sistema/Bases/Fuentes.base\|📚 Fuentes]] | Biblioteca y qué falta procesar |

## Mapas
- [[Curso de Nuevos Tutores]] — ⭐ producto principal
- [[Curso Estudiantes EN]] — futuro
- [[Estrategia de contenido]] — embudo redes → Skool gratis → pago
- [[Taxonomia]] — propiedades y valores permitidos
- [[HANDSHAKE]] — el plan completo y cómo ejecutarlo

## Rutina
- **Después de cada clase (3-5 min):** Sesión con `practicados` y `logrados` → `python 99_Sistema/scripts/arbol.py`.
- **Cada 4-6 clases por alumno:** Evaluación.
- **Semanal:** revisar el Panel de progreso, vaciar `00_Inbox`, contenido de la semana.
- **Mensual:** optimizar 1 cuello de botella, recuperar alumnos antiguos.

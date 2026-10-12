# 10 Fuentes — material bruto (solo lectura)
Libros (también los convertidos a Markdown), PDFs, epubs, manuales DELE, capturas de clases, exports de Google Sheets.

| Subcarpeta | Qué va |
|---|---|
| `Fichas/` | **Una ficha por fuente** (plantilla *Fuente*): qué es, nivel, índice de temas y a qué nodos/conceptos se conectó |
| `Libros/<Libro>/` | Cada libro en su carpeta, tal como está (no se edita) |
| `Epubs/` · `PDFs/` | Originales |
| `Capturas_clases/<alumno>/` | Capturas de las clases → se enlazan desde las sesiones |
| `Sheets/` | Exports CSV (p. ej. el Google Sheet de alumnos) |
| `Otros/` | Lo que venía en `raw/` y no encaja arriba |

- Aquí **no se escribe conocimiento**: se **conecta** desde `20_Conocimiento` (propiedad `fuentes:` con enlaces a capítulos concretos).
- Nada de esta carpeta se sube al repositorio salvo `Fichas/` (ver `.gitignore`).

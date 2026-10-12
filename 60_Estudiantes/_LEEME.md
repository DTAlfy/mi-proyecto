# 60 Estudiantes — 🔒 privado
- `Alumnos/`: una ficha por alumno (plantilla *Alumno*): `nivel_base`, `dominados`, `meta`.
- `Sesiones/`: una nota por clase (plantilla *Sesión*), nombre `AAAA-MM-DD Nombre`, con `practicados` y `logrados`.
- `Evaluaciones/`: cada 4-6 clases (plantilla *Evaluación*), con `logrados`.
- `Arboles/`: **generado** por `python 99_Sistema/scripts/arbol.py` → árbol (.html y .canvas), ruta y [[Panel de progreso]].

Nada de esto se sube al repositorio (ver `.gitignore`), salvo los alumnos ficticios **Demo** (Emma, Jake, Lucía),
que están para que veas el sistema funcionando. Bórralos cuando tengas alumnos reales.

Para migrar el Google Sheet: expórtalo como CSV a `10_Fuentes/Sheets/` y pide a Claude que cree las fichas.

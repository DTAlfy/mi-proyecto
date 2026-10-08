# SpanishWithAlfy Mentoring

Pipeline que produce el curso "De $5/h a $25/h: Tutor de Español Online". Alfy solo graba leyendo en OBS;
el repo genera guiones, visuales (Apimart), voces (ElevenLabs), teleprompter, edición DaVinci y workbooks.

Fuentes de verdad: `00_Sistema/curriculum.yaml` (lecciones), `00_Sistema/materiales.yaml` (entregables),
`00_Sistema/config.yaml` (proveedores, voces, marca, presupuesto). Formato de guion: `docs/FORMATO_GUION.md`.
Skills: `/guion`, `/materiales`, `/produccion`, `/captacion`.

## Reglas
- **Nunca uses `--generar` ni `comparar-voces` sin un "sí" explícito de Alfy en ese mensaje** (gastan saldo). Antes, dry-run con `--breve`.
- No leas `.env`.
- Nombres: `M[XX]_L[XX]_[Clave]_[TIPO]`, Clave en CamelCase ASCII. En código, usa siempre `swa/naming.py`.
- Para contexto de lecciones usa `python builder.py contexto MM [LL]`, no los YAML completos. No releas archivos generados: la CLI informa.
- Sin cifras ni testimonios inventados: `[NOTA: verificar …]`.
- `00_Sistema/scripts/resolve/` corre dentro de DaVinci gratis: solo librería estándar.
- Cambios de código → tests en `00_Sistema/tests/` (`python -m pytest 00_Sistema/tests -q`).

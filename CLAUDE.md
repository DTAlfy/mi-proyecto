# SpanishWithAlfy Mentoring: contexto para Claude Code

Pipeline que automatiza la producción de un curso en video para **tutores de español online que empiezan**
(promesa: pasar de $5/h a $25/h en Preply/italki). Alfy solo graba leyendo guiones en OBS (pantalla + cámara).
Lo demás (guiones, visuales, teleprompter, edición, render y workbooks) lo genera este repo.

## Fuentes de verdad (léelas antes de generar nada)
- `00_Sistema/curriculum.yaml`: módulos, lecciones, `clave` de cada archivo, objetivos e hitos del roadmap.
- `00_Sistema/config.yaml`: rutas, proveedores (Apimart / ElevenLabs), modelos, marca y presupuesto.
- `docs/FORMATO_GUION.md`: estructura pedagógica y etiquetas `[BROLL]`, `[IMG]`, `[SLIDE]`, `[ROADMAP]`, `[PANTALLA]`, `[AUDIO]`, `[TAREA]`, `[RECURSO]`.

## Nomenclatura (estricta, la ingesta depende de ella)
`M[XX]_L[XX]_[Clave]_[TIPO]` con `Clave` en CamelCase ASCII sin tildes ni ñ.
Ejemplos: `01_Guiones/M01_L01_Nicho.md`, `02_Bruto_OBS/M01_L01_Nicho_RAW.mp4`,
`03_Assets_Generados/BROLL/M01_L01_001.mp4`, `05_Renders_Finales/M01_L01_Nicho_FINAL.mp4`.
Nunca construyas nombres a mano en código: usa `swa/naming.py`.

## Comandos
```bash
python builder.py validar [MM LL]          # siempre después de escribir/editar un guion
python builder.py preparar MM LL           # dry-run de assets + teleprompter + checklist
python builder.py preparar MM LL --generar # GASTA SALDO de Apimart/ElevenLabs
python builder.py editar MM LL             # tras grabar: Auto-Cut + plan para DaVinci
python builder.py workbook M               # PDF del módulo
python builder.py estado                   # avance de todas las lecciones
python -m pytest 00_Sistema/tests -q       # tests (sin APIs ni DaVinci)
```

## Reglas para Claude
- **Nunca ejecutes `--generar` ni `comparar-voces` sin confirmación explícita de Alfy en ese mismo mensaje.** Cuestan dinero.
  Enseña antes el dry-run con el número de llamadas y el coste estimado.
- No leas ni muestres `.env`. Las claves solo se leen en `swa/config.py::secreto`.
- Guiones en español neutro, frases de 20 palabras como máximo, hablando a UNA persona (tú). Prompts de `[BROLL]`/`[IMG]` en inglés, de 3 a 6 palabras, sin texto en la imagen.
- Texto en pantalla (títulos, listas): `[SLIDE]` local (gratis y nítido), nunca `[IMG]`.
- No inventes datos ni estadísticas de plataformas. Si hace falta un dato, deja `[NOTA: verificar dato X]`.
- Los scripts de `00_Sistema/scripts/resolve/` corren dentro de DaVinci Resolve **gratis** (Workspace › Scripts):
  solo librería estándar de Python y la API de Resolve, sin dependencias externas.
- Cambios de código: añade o ajusta tests en `00_Sistema/tests/` y pásalos antes de hacer commit.

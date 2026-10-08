# Calendario de creación del curso: del 9 de octubre al 13 de noviembre de 2026

**Supuesto:** unas 3 horas al día, de lunes a viernes. Los fines de semana quedan libres como **colchón**:
si un día se retrasa, recupéralo el sábado y no muevas el resto del calendario.
Cada día termina con un **entregable** que puedes comprobar. Detalle de cada fase: `docs/PLAN_DE_PRODUCCION.md`.

---

## Semana 1: arranque

### Viernes 9 oct · Día 1 · Preparar el PC
- [ ] Instalar Python 3.12, ffmpeg (`winget install Gyan.FFmpeg`), OBS y DaVinci Resolve (gratis)
- [ ] Clonar el repo en `C:\SpanishWithAlfy_Mentoring` → `pip install -r requirements.txt`
- [ ] `python -m pytest 00_Sistema/tests -q` → todo en verde
- [ ] `python builder.py instalar-davinci` y reiniciar Resolve
- [ ] `python builder.py web` → abre `04_Workbooks/Web/index.html` y prueba los 7 materiales
- **Entregable:** `python builder.py estado` muestra los 27 guiones ✓ y los scripts SWA aparecen en DaVinci.

*Sábado y domingo (opcional):* lee en voz alta M01_L01 y M01_L02 para encontrar tu ritmo.

## Semana 2: configuración y lección piloto

### Lunes 12 oct · Día 2 · Escenas de OBS
- [ ] Seguir `docs/GUIA_GRABACION_OBS.md`: perfil `SWA`, escenas `Camara`, `Clase` y `Pantalla`, filtros del micrófono y atajos
- [ ] Prueba de 30 s en cada escena: luz, sonido, encuadre y cambio de escena con Ctrl+Alt+1/2
- **Entregable:** un clip de prueba con audio limpio y cambio de escena.

### Martes 13 oct · Día 3 · Cuentas, claves y voces
- [ ] Cuentas de Apimart y ElevenLabs → claves en `.env`
- [ ] Verificar rutas y modelos de Apimart (`docs/PROVEEDORES.md`) y rellenar `costos_usd` en `config.yaml`
- [ ] Elegir las 5 voces en la Voice Library de ElevenLabs y pegar sus IDs en `config.yaml`
- [ ] `python builder.py comparar-voces "Hi! I'm your Spanish tutor. Nice to meet you." --voz modelo_en`
- [ ] Marca y enlaces en `config.yaml` (colores, Skool, TidyCal, checkout)
- **Entregable:** dos audios de prueba que te gustan y `python builder.py materiales --breve` con el coste en dólares.

### Miércoles 14 oct · Día 4 · Materiales entregables
- [ ] `python builder.py materiales MAT01 --generar` → **una sola** prueba; revisa la ilustración
- [ ] Si te gusta: `python builder.py materiales --generar` (ilustraciones, fondos, 9 materiales y 16 audios)
- [ ] Verificar las horas del Mapa MCER con el Instituto Cervantes → `verificado: true` en MAT01
- [ ] `python builder.py web --capturas` → revisa la práctica de inglés (WEB07), que ya debería sonar
- **Entregable:** `04_Workbooks/Materiales/` (9 PNG), `Audios/` (16 MP3) y `Web/` completos.

### Jueves 15 oct · Día 5 · Piloto: preparar y grabar M01_L01
- [ ] Leer el guion en voz alta, ajustarlo a tu forma de hablar y marcar `estado: revisado`
- [ ] `python builder.py preparar 01 01 --breve` → `--generar`
- [ ] Grabar con el teleprompter y el checklist → `02_Bruto_OBS/M01_L01_Nicho_RAW.mp4`
- **Entregable:** el archivo RAW de la lección piloto.

### Viernes 16 oct · Día 6 · Piloto: editar y renderizar
- [ ] `python builder.py editar 01 01` → DaVinci: SWA 1 - Montar leccion → revisar → SWA 2 - Render
- [ ] Ver el video completo y apuntar ajustes (umbral del Auto-Cut, duración de slides, zoom, estilo visual)
- [ ] Aplicar los ajustes en `config.yaml` y repetir `editar` si hace falta (la transcripción está en caché)
- **Entregable:** `05_Renders_Finales/M01_L01_Nicho_FINAL.mp4` que publicarías tal cual.

## Semana 3: revisión de guiones y assets

### Lunes 19 oct · Día 7 · Revisar M01 y M02 (7 lecciones)
- [ ] Leer en voz alta, cambiar lo que no suene a ti y resolver cada `[NOTA: verificar …]`
- [ ] `python builder.py validar` → `estado: revisado` en cada una

### Martes 20 oct · Día 8 · Revisar M03 y M04 (7 lecciones)
- [ ] Igual que ayer. Comprueba tus demos `[PANTALLA]`: ¿tienes las cuentas y las páginas necesarias?

### Miércoles 21 oct · Día 9 · Revisar M05, M06 y M07 (12 lecciones, más cortas de revisar)
- [ ] Igual. En M07 escucha los audios del pack mientras revisas.
- **Entregable:** los 27 guiones en `estado: revisado` y `validar` sin errores.

### Jueves 22 oct · Día 10 · Assets en lote
- [ ] Por módulo: `python builder.py preparar MM LL --breve` → `--generar`
- [ ] Revisar cada B-Roll e imagen; si uno no sirve, cambia solo su prompt en el guion y regenera (la caché protege el resto)
- **Entregable:** `python builder.py estado` con todos los assets en `N/N`.

### Viernes 23 oct · Día 11 · Sesión de grabación 1: M01 (L02-L04)
- [ ] Rutina de 10 min de `docs/GUIA_GRABACION_OBS.md` §5 → grabar las 3 lecciones
- [ ] Renombrar los archivos con el nombre exacto del checklist
- **Entregable:** 3 RAW nuevos (`python builder.py validar` comprueba los nombres).

## Semana 4: grabación (misma ropa, luz y encuadre cada día)

| Día | Fecha | Sesión | Lecciones |
|---|---|---|---|
| 12 | Lunes 26 oct | 2 | M02 (L01-L04) |
| 13 | Martes 27 oct | 3 | M03 (L01-L03) + M07_L01 |
| 14 | Miércoles 28 oct | 4 | M04 (L01-L04) |
| 15 | Jueves 29 oct | 5 | M05 (L01-L03) + M07_L02-L03 |
| 16 | Viernes 30 oct | 6 | M06 (L01-L04) + M07_L04-L05 |

- **Entregable de la semana:** los 27 RAW grabados y bien nombrados.

## Semana 5: postproducción y workbooks

Por cada lección: `python builder.py editar MM LL` → SWA 1 → revisar marcadores (azul = pantalla,
rojo = falta asset) → borrar tomas repetidas → SWA 2. Unos 20-30 min por lección.

| Día | Fecha | Lecciones |
|---|---|---|
| 17 | Lunes 2 nov | M01 (L02-L04) + M02 (4) |
| 18 | Martes 3 nov | M03 (3) + M04 (4) |
| 19 | Miércoles 4 nov | M05 (3) + M06 (4) |
| 20 | Jueves 5 nov | M07 (5) + repetir lo que haya quedado mal |

### Viernes 6 nov · Día 21 · Workbooks y control de calidad
- [ ] Capturas de Lightshot/Flameshot en `03_Assets_Generados/CAPTURAS/M[XX]_L[XX]_*.png`
- [ ] `python builder.py workbook 1` … `7` y `python builder.py web --capturas`
- [ ] Ver los 27 videos a 1,5x con una lista de errores; corregir los graves
- **Entregable:** 27 `_FINAL.mp4`, 7 workbooks PDF y el centro de materiales web.

## Semana 6: lanzamiento

### Lunes 9 nov · Día 22 · Aula en Skool
- [ ] Crear el aula: 7 módulos, 27 lecciones con su video
- [ ] Adjuntar a cada módulo su workbook PDF, sus materiales PNG, sus audios y su carpeta `Web/` (o el `index.html`)
- **Entregable:** el curso completo navegable en Skool.

### Martes 10 nov · Día 23 · Cobros y mentoría
- [ ] Producto en Gumroad o Stripe (curso self-paced)
- [ ] TidyCal: "Auditoría de Perfil 1 a 1"
- [ ] Enlaces definitivos en `config.yaml` → regenerar workbooks (`workbook 1`…`7`) y volver a subirlos
- **Entregable:** una compra de prueba que da acceso a Skool.

### Miércoles 11 nov · Día 24 · Lead magnet y página de ventas
- [ ] `/captacion lead-magnet` y `/captacion ventas` en Claude Code → revisar y publicar
- **Entregable:** página de ventas publicada y lead magnet funcionando.

### Jueves 12 nov · Día 25 · Contenido de captación
- [ ] `/captacion shorts` → 5 guiones de Shorts/Reels "antes y después" con un único CTA
- [ ] Grabar los 5 en una sesión con la escena `Camara`
- **Entregable:** 5 Shorts listos para publicar (uno cada dos días).

### Viernes 13 nov · Día 26 · Último día de creación
- [ ] Recorrer el embudo completo como si fueras un alumno: Short → lead magnet → página de ventas → compra → Skool → TidyCal
- [ ] Corregir lo que falle, publicar el primer Short y abrir la comunidad
- **Entregable:** 🎉 curso publicado y embudo funcionando.

---

### Después del lanzamiento (rutina semanal)
- Lunes: tus 5 números en el diagnóstico (WEB02) y en el panel de Skool
- Un Short nuevo cada dos días (`/captacion shorts`)
- Responder en la comunidad de Skool en un bloque fijo de 30 minutos al día
- Cada mes: mejorar la lección con más abandonos (`/guion MM LL` + regrabar solo esa)

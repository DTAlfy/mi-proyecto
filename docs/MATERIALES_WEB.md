# Materiales web interactivos

Complementan los PNG y los PDF con herramientas que el alumno **usa**, no solo mira.
Cada material es **un único archivo HTML** (CSS y JS incrustados, sin dependencias):
se abre con doble clic, funciona sin conexión, se puede subir a Skool o enviar por correo,
tiene modo claro/oscuro, se adapta al móvil, se puede imprimir y guarda el progreso en el navegador del alumno.

```bash
python builder.py web             # 04_Workbooks/Web/*.html + index.html (centro de materiales)
python builder.py web --capturas  # además, PNG 1920x1080 de cada página (para el video o las redes)
```
Coste: $0 (no usa APIs).

## Catálogo actual (`00_Sistema/web.yaml`)

| Id | Material | Componente | Módulo | Uso |
|---|---|---|---|---|
| WEB01 | Calculadora de ingresos: tu camino a $1000/mes | calculadora | 1 | Precio neto, horas necesarias por escalón |
| WEB02 | Diagnóstico: ¿en qué etapa estás? | diagnostico | 1 | 5 números → etapa, prioridad e historial semanal |
| WEB03 | Checklist "De 0 a Tutor PRO" | hitos | 1 | 29 acciones de las 6 etapas, con progreso |
| WEB04 | Generador de titulares | titular | 2 | Versiones ES/EN listas para copiar |
| WEB05 | Cronómetro de la clase de prueba | cronometro | 3 | Fases de 30 min con aviso sonoro y frases |
| WEB06 | Mapa MCER interactivo | niveles | 4 | Nivel, horas orientativas, exámenes e inglés recomendado |
| WEB07 | Práctica de inglés de aula | tarjetas | 7 | Shadowing (AUD02) y listening (AUD01) con audio |

Los datos que ya existen en `materiales.yaml` (MCER, clase de prueba, packs de audio) se leen con
`fuente:`: si cambias un dato allí, cambian a la vez el PNG, el PDF y la página web.

## Crear un material nuevo
1. Copia una entrada de `web.yaml`, cambia `id` (WEB08…), `clave`, `titulo` (`*palabra*` = destacada), `lead` y `datos`.
2. `python builder.py web WEB08` y ábrelo en el navegador.
3. Si necesitas un componente nuevo, se añade una función en `00_Sistema/templates/web/swa.js` (registrada en `COMPONENTES`) y su nombre en `swa/web.py`.

## En los videos
- Demo en directo: `[PANTALLA: Calculadora de ingresos WEB01 …]` (escena *Clase*).
- Como visual fijo: usa la captura `04_Workbooks/Web/capturas/WEBxx_….png`.

## Diseño
Tokens en `:root` (colores de marca inyectados desde `config.yaml`), tipografía Fraunces + Inter
(con fuentes del sistema si no hay conexión), modo oscuro automático y manual, foco visible,
`prefers-reduced-motion` y estilos de impresión.

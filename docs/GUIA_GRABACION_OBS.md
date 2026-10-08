# Guía de OBS: escenas y grabación

Objetivo: un archivo por lección, con audio limpio y tres escenas que el teleprompter te indica cuándo usar.
Todo se configura **una sola vez** (unos 45 minutos).

## 1. Perfil y colección de escenas

En OBS: **Perfil › Nuevo** → `SWA` y **Colección de escenas › Nueva** → `SWA`.
Así esta configuración no se mezcla con otras que uses.

**Ajustes › Video**
- Resolución base (lienzo) y de salida: **1920x1080**
- FPS: **30**

**Ajustes › Salida** (modo Avanzado) › Grabación
- Formato: **MKV** + en *Ajustes › Avanzado* activa **Remux automático a MP4** (si OBS se cierra de golpe, el MKV no se corrompe)
- Codificador: el de hardware (NVENC, AMF o QuickSync)
- Pistas de audio: solo la **1**

**Ajustes › Audio**
- Audio de escritorio: **Desactivado** (así no se graban notificaciones). Actívalo solo si una demo necesita sonido.
- Micrófono/Auxiliar: tu micrófono.

**Filtros del micrófono** (clic derecho › Filtros), en este orden:
1. Supresión de ruido: RNNoise
2. Puerta de ruido: cerrar a -45 dB, abrir a -35 dB (el silencio queda por debajo del umbral del Auto-Cut)
3. Compresor: ratio 4:1, umbral -18 dB
4. Limitador: -1 dB

## 2. Las tres escenas

El nombre de cada escena debe ser exactamente el que usa el teleprompter (`config.yaml › obs`).

### Escena `Camara` (por defecto: hook, explicaciones y cierre)
| Fuente | Tipo | Ajuste |
|---|---|---|
| `Cam` | Dispositivo de captura de video | Clic derecho › Transformar › **Ajustar a la pantalla** (Ctrl+F) |

Encuadre: ojos en el tercio superior, hombros visibles, luz frontal.

### Escena `Clase` (se activa en cada `[PANTALLA]`)
| Fuente | Tipo | Ajuste |
|---|---|---|
| `Navegador` | **Captura de ventana** (la ventana de Chrome/Edge con la demo) | Ajustar a la pantalla (Ctrl+F) |
| `Cam` | *Agregar existente* › `Cam` | Tamaño **480x270**, posición **x 1400 · y 770** (esquina inferior derecha, 40 px de margen) |

Esquinas redondeadas para la cámara: en `Cam` dentro de esta escena › Filtros › **Máscara de imagen/mezcla**,
tipo *Máscara alfa (canal de color)*, imagen `00_Sistema/templates/obs/mascara_camara_480x270.png`.

> Usa **captura de ventana**, no de pantalla completa: así el teleprompter (en otra ventana) nunca sale en el video.

### Escena `Pantalla` (opcional: demos donde la cámara tape algo)
| Fuente | Tipo | Ajuste |
|---|---|---|
| `Navegador` | *Agregar existente* › `Navegador` | Ajustar a la pantalla |

## 3. Atajos de teclado

**Ajustes › Atajos**. Usa combinaciones que no choquen con el navegador:

| Acción | Atajo |
|---|---|
| Escena `Camara` | Ctrl+Alt+1 |
| Escena `Clase` | Ctrl+Alt+2 |
| Escena `Pantalla` | Ctrl+Alt+3 |
| Iniciar/detener grabación | Ctrl+Alt+R |

## 4. Teleprompter

Abre `01_Guiones/teleprompter/M.._TELEPROMPTER.html`:
- **En otra ventana o en una tablet/móvil junto a la cámara**, nunca dentro de la ventana que capturas.
- **Espacio**: iniciar/pausar · **↑/↓**: velocidad · **+/−**: tamaño · **M**: espejo (teleprompter de cristal)
- Cápsula amarilla **🎥 Cambia a escena: X** → pulsa el atajo de esa escena.
- Cápsula azul **🖥 Muestra: …** → lo que tienes que enseñar en la ventana del navegador.
- Las demás (B-Roll, Slide, Objetivos, Audio…) son informativas: se insertan solas en la edición.
- **🔊 Audio**: no hagas pausa. El pipeline detiene el video y reproduce el audio en la edición.

## 5. Rutina de cada sesión de grabación (10 minutos)

1. Agua, luz frontal encendida y notificaciones del sistema desactivadas (modo concentración).
2. Abre el checklist de la lección: `01_Guiones/teleprompter/M.._CHECKLIST.md`.
3. Abre en el navegador, en pestañas y en orden, todo lo que lista "Ten abierto en pantalla".
4. Prueba de sonido de 10 s: los picos del micrófono, entre -12 y -6 dB.
5. Escena `Camara` → Ctrl+Alt+R → 2 s de silencio → empieza a leer.

**Si te equivocas:** pausa de 2 s, una palmada y repite la frase entera. El Auto-Cut elimina la pausa;
la palmada es un pico visible en la forma de onda y te dice qué toma borrar en DaVinci.

## 6. Después de grabar

1. Renombra el archivo a `02_Bruto_OBS/M01_L01_Nicho_RAW.mp4` (el nombre exacto está en el checklist).
2. `python builder.py editar 01 01` (o `/produccion editar 01 01` en Claude Code).
3. DaVinci › Workspace › Scripts › **SWA 1 - Montar leccion** → revisar → **SWA 2 - Render**.

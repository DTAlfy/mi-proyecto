# Guía de grabación con OBS (pantalla + cámara)

Objetivo: un único archivo por lección, con audio limpio, que el Auto-Cut pueda procesar sin retoques.

## Configuración (una sola vez)

**Ajustes › Video**
- Resolución base y de salida: 1920x1080
- FPS: 30 (o 60 si haces demos con mucho movimiento; el pipeline lee el FPS real del archivo)

**Ajustes › Salida › Grabación**
- Formato: **MKV** con *Ajustes › Avanzado › Remux automático a MP4* activado (si OBS se cuelga, el MKV no se corrompe)
- Codificador: el de hardware (NVENC/AMF/QuickSync) y calidad "Indistinguible"
- Pistas de audio: solo la 1 (micrófono)

**Ajustes › Avanzado**
- Formato del nombre de archivo: `%CCYY-%MM-%DD_%hh-%mm` (luego lo renombras con la nomenclatura)

**Filtros del micrófono** (clic derecho › Filtros), en este orden:
1. Supresión de ruido (RNNoise)
2. Puerta de ruido: cerrar -45 dB, abrir -35 dB. Así el silencio queda bajo el umbral del Auto-Cut (-35 dB)
3. Compresor 4:1, umbral -18 dB
4. Limitador -1 dB

## Escena "Clase"
- **Captura de pantalla** (o de ventana del navegador) a pantalla completa
- **Cámara** en la esquina inferior derecha, alrededor del 22 % del ancho, con borde redondeado (filtro "Máscara de imagen")
- Escena extra "Solo cámara" para el hook y el cierre (cámbiala con una tecla rápida)

## Teleprompter
Abre `01_Guiones/teleprompter/M.._TELEPROMPTER.html` en una ventana pegada a la cámara:
- **Espacio**: iniciar/pausar · **↑/↓**: velocidad · **+/−**: tamaño · **M**: espejo (para teleprompter de cristal)
- Las cápsulas azules **🖥 Muestra:** te dicen qué enseñar en pantalla en ese momento.
- Los demás avisos (B-Roll, Slide...) son solo informativos: se insertan en la edición.

## Durante la grabación
- Si te equivocas: **pausa de 2 s, palmada y repite la frase entera.** El Auto-Cut elimina la pausa; la palmada se ve como un pico en la forma de onda y marca la toma que tienes que borrar.
- No hables sobre el clic del ratón: haz clic, pausa y habla.
- Deja 2 s de silencio al principio y al final.

## Después
1. Renombra el archivo a `02_Bruto_OBS/M01_L01_Nicho_RAW.mp4` (el nombre exacto está en el checklist).
2. `python builder.py editar 01 01`

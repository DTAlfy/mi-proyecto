# Sistema de Plantillas Profesionales en PowerPoint (Template OS con Macros VBA)

## 🎯 Objetivo Principal
Construir, escalar y mantener plantillas de PowerPoint modulares y altamente consistentes utilizando un "Sistema Operativo de Plantillas" basado en automatización con Macros VBA, retículas estrictas y nomenclatura de objetos, permitiendo cambios globales en cientos de slides en segundos.

## 🛠️ Herramientas y Entorno Necesario
- **Software:** Microsoft PowerPoint (Versión de escritorio Windows/Mac con soporte para Macros).
- **Motor de Automatización:** Editor de Visual Basic (VBA) y Macros.
- **Rol de la IA:** Generar los códigos VBA si el usuario no los tiene, proponer paletas de colores (HEX), tipografías y redactar el contenido estructurado para los componentes (tarjetas, agendas, infografías).

## ⚙️ Flujo de Trabajo (Paso a Paso)

### 1. Configuración del Lienzo (Grid Maker)
- Activar la pestaña "Programador/Desarrollador" en PPT.
- Insertar un módulo VBA y pegar el código del "Grid Maker".
- Definir parámetros (ej. 12 columnas, 8 filas, márgenes de 30pt) y ejecutar la macro para generar guías a nivel de Slide Master.

### 2. Definición del Tema (Colores y Fuentes)
- **Colores:** Ingresar códigos HEX en cuadros de texto designados y ejecutar la macro "Theme Colors" para inyectarlos en la paleta nativa del tema de PPT.
- **Fuentes:** Cambiar la tipografía en los cuadros de texto de referencia (Heading/Body) y correr la misma macro para actualizar las fuentes maestras de toda la presentación.

### 3. Sistema de Componentes y Nomenclatura (El Núcleo del Sistema)
- **Estilos Globales (Card Styles / Text Styles):** Se basan estrictamente en el **Panel de Selección**.
- La macro busca prefijos específicos (ej. `label_2`, `title_style`, `card_2`) en los objetos de las slides y les aplica el formato del objeto "maestro" que comparte ese mismo nombre en la slide de estilos.
- **Placeholders de Imagen:** Dibujar cualquier forma, seleccionarla y correr la macro "Image Placeholder" para crear automáticamente un layout maestro con ese placeholder funcional.
- **Custom Footer:** Estiliza los placeholders nativos de fecha, pie de página y número de slide en el Slide Master basándose en formas de referencia (ej. rectángulos redondeados).

### 4. Animaciones en Lote (Animation Delay)
- Copiar animaciones de una librería maestra usando el "Copiar Animación" (o `Alt+Shift+C`).
- **Truco del Retardo Incremental:** Crear un cuadro de texto temporal con el valor del retardo deseado (ej. `0.2`), seleccionarlo, seleccionar las animaciones en el Panel de Animación y ejecutar la macro de "Delay". Esto aplica retardos secuenciales automáticos a múltiples objetos.

## 📏 Reglas de Oro y Restricciones
- ⚠️ **Formato de Archivo Crítico:** El archivo debe guardarse como **Presentación habilitada para macros (.PPTM)**. Si se guarda como `.PPTX`, todo el código VBA y los botones de acceso rápido se perderán irremediablemente.
- ⚠️ **Regla de Nomenclatura:** Nunca cambiar los prefijos en el Panel de Selección (ej. `label_`, `card_`, `title_`) si se desea que las macros de estilos globales funcionen. El sufijo (ej. un número o signo de exclamación) no importa, solo el prefijo.
- ⚠️ **Excepción de Color (Keep Color):** Si un texto debe mantener un color específico (ej. texto blanco sobre una tarjeta oscura) al actualizar los estilos globales de texto, se debe añadir la palabra `keep color` al final del nombre del objeto en el Panel de Selección. La macro actualizará la fuente y el tamaño, pero ignorará el color.
- **Alineación:** Respetar siempre los márgenes y la retícula (Atajo `Alt+F9` o `Cmd+F9` para ver/ocultar guías).
- **Acceso Rápido:** Asignar las macros a la Barra de Herramientas de Acceso Rápido con iconos personalizados para acelerar el flujo de trabajo.

## 💡 Prompts Clave (Para interactuar con la IA)
- **Para generar código VBA:** *"Actúa como un experto en VBA para PowerPoint. Escríbeme el código para una macro que busque todos los objetos en el Panel de Selección que empiecen con 'card_2' y les aplique el relleno y borde del objeto maestro llamado 'card_2_master'."*
- **Para estructurar contenido:** *"Tengo un componente de 'Tarjeta de Métricas' (card_2). Dame 3 títulos cortos, 3 valores numéricos grandes y 3 descripciones breves sobre [TEMA] que encajen en este formato."*
- **Para paletas de colores:** *"Dame 6 códigos HEX para una plantilla de PowerPoint con estética [Ej. Corporativo Suizo] incluyendo fondos, acentos y modo oscuro."*

## 📤 Estructura de Salida (Arquitectura de Slides en PPT)
- **Slide Master / Layouts:** Contenedores limpios con placeholders generados por macros (Logos posicionados, Imágenes, Footers estilizados).
- **Slide de Estilos (Dashboard):** Slide de referencia (usualmente oculta al presentar) que contiene los objetos maestros (`title_style`, `card_1`, `card_2`, `label_1`) donde se dictan las reglas visuales globales.
- **Slides de Contenido:** Slides limpias donde solo se "pegan" componentes desde la librería, asegurando que hereden los nombres del Panel de Selección para futuras actualizaciones globales.
- **Librería de Animaciones:** Slide de referencia con objetos pre-animados que sirven como fuente para el "Animation Painter".
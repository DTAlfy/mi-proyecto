# Title Slide Moderno con Efecto Glow y Ondas Animadas (Estilo Tech)

## 🎯 Objetivo Principal
Diseñar una diapositiva de título (Title Slide) de alto impacto visual con estética oscura (dark mode), integrando tipografía con degradado, botones con efecto de vidrio esmerilado (frosted glass) y líneas onduladas brillantes animadas en la parte inferior.

## 🛠️ Herramientas y Entorno Necesario
- **Software Principal:** Microsoft PowerPoint.
- **Software Vectorial de Apoyo:** Affinity Designer (de Canva) o Illustrator para trazar curvas precisas que PPT no puede hacer nativamente con exactitud.
- **Tipografía:** "Unbounded" (Google Fonts) u otra fuente geométrica moderna.
- **Rol de la IA:** Generar el *copy* ultracorto para títulos y botones, y sugerir paletas de colores HEX para los degradados neón.

## ⚙️ Flujo de Trabajo (Paso a Paso)

### 1. Configuración de Fondo y Tipografía
- **Fondo:** Relleno sólido negro.
- **Título:** Fuente Unbounded (96pt), alineación centrada.
- **Ajustes de Texto:** Interletraje condensado (-3pt) e interlineado múltiple (0.8 o 0.9) para compactar el bloque.
- **Degradado de Texto:** Relleno de degradado lineal. Blanco (posición 50%) a Azul `#0066FF`.

### 2. Botón "Frosted" (Píldora)
- **Forma:** Rectángulo redondeado al máximo (tirar del controlador amarillo).
- **Ajustes Internos:** Desactivar "Ajustar texto a la forma". Márgenes internos: 0.4" (Izq/Der) y 0.2" (Sup/Inf).
- **Relleno:** Degradado de Azul a Verde `#00FF99` (Azul al 70%). Sin borde/línea.
- **Efecto Vidrio (Frosted):** Aplicar **Sombra Interior** (Inner Shadow) color Blanco, 0% de transparencia y 15pt de desenfoque (blur).

### 3. Trazado de Ondas (Flujo Vectorial Externo)
- **En Affinity/Illustrator:** Crear lienzo Full HD, activar reglas y guías. Usar la Pluma (Pen Tool) con *snapping* para crear 7 puntos entre las guías.
- **Optimización:** Seleccionar todos los nodos, distribuir horizontalmente y convertir a "Smooth" (suavizar) para crear la curva perfecta. Eliminar nodos de los extremos.
- **Importación a PPT:** Copiar, pegar en PPT y usar **"Convertir a forma"** para poder editarla nativamente.
- **Ajuste Crítico:** Fijar el ancho de la forma en **960 puntos** (el ancho exacto por defecto de una slide PPT) para que cubra el 100% del lienzo sin descuadres.

### 4. Estilizado de Ondas (Efecto Glow/Neón)
Duplicar la onda base (`Ctrl + Shift + Arrastrar`) y aplicar los siguientes estilos de línea y efectos:
- **Onda 1 (Azul):** 30pt de grosor. Sombra exterior (Azul, 100% tamaño, 70pt blur). Resplandor/Glow (Azul, 150pt tamaño, 85% transparencia).
- **Onda 2 (Verde):** 15pt de grosor. Sombra y Glow verde (Glow de 50pt tamaño).
- **Onda 3 (Blanca):** 5pt de grosor. Sombra y Glow blanco (Glow de solo 15pt tamaño para no "quemar" la imagen).

### 5. Animación de Entrada
- **Título y Botón:** Animación "Desvanecer" (Fade), duración 1-2s. El botón debe tener un **retardo de 0.5s**.
- **Ondas:** Animación de entrada (ej. "Entrar volando" / Fly In), duración 2s, "Iniciar con la anterior". En *Opciones de Efectos*, activar **"Final suave" (Smooth end)**.

## 📏 Reglas de Oro y Restricciones
- ⚠️ **Simulación de Frosted Glass:** PowerPoint no tiene un desenfoque de fondo (background blur) nativo en tiempo real para formas. El truco definitivo es usar la *Sombra Interior* blanca con desenfoque sobre un fondo degradado para engañar al ojo.
- ⚠️ **Proporción del Glow Blanco:** El color blanco emite mucha luz por sí solo. Su efecto Glow debe ser drásticamente menor (15pt) comparado con colores oscuros (150pt) para evitar que se vea como una mancha quemada.
- ⚠️ **Ancho de Slide:** Usar siempre la medida de **960 puntos** para elementos que deban cruzar la slide de extremo a extremo horizontalmente, evitando que PowerPoint redimensione las formas al cambiar de equipo.
- **Edición de Nodos:** Nunca intentes dibujar curvas complejas con la herramienta "Forma Libre" o "Curva" de PPT si buscas precisión matemática; usa siempre un software vectorial y convierte a forma al importar.

## 💡 Prompts Clave (Para interactuar con la IA)
- **Para copy de Title Slide:** *"Necesito el texto para un Title Slide de tecnología. Dame 3 opciones de título principal (máximo 3 palabras, para aplicar interletraje condensado) y 3 opciones para un botón tipo píldora (máximo 2 palabras, tono disruptivo)."*
- **Para paletas neón:** *"Dame 3 pares de códigos HEX para crear degradados neón de alto contraste sobre fondo negro. Un color debe ser cálido y el otro frío (ej. cian y magenta)."*

## 📤 Estructura de Salida (Arquitectura de la Slide)
- **Capa 0 (Fondo):** Negro sólido `#000000`.
- **Capa 1 (Gráficos Base):** 3 líneas onduladas apiladas en el tercio inferior de la slide (Z-index bajo).
- **Capa 2 (UI/Texto):** Título centrado en el eje vertical superior/medio. Botón píldora ubicado justo debajo del título, respetando la retícula central.
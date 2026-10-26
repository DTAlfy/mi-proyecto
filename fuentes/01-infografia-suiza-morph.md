# Infografías Animadas Minimalistas (Estilo Suizo) con Transición Morph

## 🎯 Objetivo Principal
Diseñar y animar una infografía minimalista de estilo "Swiss Design" (Diseño Suizo) nativamente en PowerPoint, utilizando formas geométricas, ilusiones de espacio negativo y la transición "Morph" (Transformación) para crear un recorrido visual fluido y profesional sin usar animaciones complejas.

## 🛠️ Herramientas y Entorno Necesario
- **Software:** Microsoft PowerPoint (Nativo).
- **Recursos Externos:** Siluetas o iconos en formato `.SVG` (para poder desagrupar y editar).
- **Rol de la IA:** Generar la narrativa (copy), los hitos del recorrido (steps) y sugerir la distribución de los textos para que el usuario los coloque en la plantilla de PowerPoint.

## ⚙️ Flujo de Trabajo (Paso a Paso)

### 1. Configuración de Lienzo y Retícula
- **Fondo:** Usar un color blanco roto/amarillento suave (ej. paleta Office 2007-2010) para reducir la fatiga visual.
- **Guías:** Activar las guías (`Vista > Guías`). Idealmente, usar una retícula de 12 columnas con márgenes de 30pt (se puede hacer con macros o manualmente).

### 2. Construcción de los "Muros" (El Camino)
- **Forma Base:** Insertar un **Paralelogramo**.
- **Transformación:** Rotar 90° a la derecha y luego Voltear Horizontalmente para crear la inclinación correcta.
- **Progresión:** Duplicar la forma (`Ctrl + Shift + Arrastrar`) y reducir su altura progresivamente (ej. 12cm -> 9cm -> 6cm -> 3cm). Alinear los bordes para que formen un camino continuo.

### 3. Aplicación de Degradados (Gradientes)
- **Configuración:** Relleno de degradado con solo 2 paradas de color (ej. Naranja y Azul).
- **Ajuste de Ángulo:** Modificar el ángulo del degradado (ej. 15°) para que las líneas de color sigan la inclinación del paralelogramo.
- **Optimización:** Copiar y pegar el estilo (`Ctrl + Shift + C / V`) entre los muros y ajustar ligeramente las posiciones de las paradas de color para dar variedad. *Eliminar siempre el contorno (línea) de las formas.*

### 4. Ilusión de Espacio Negativo (El Camino Superior)
- **Trazado:** Usar la herramienta **Forma Libre** (Freeform) para trazar una línea sobre los bordes superiores de los muros.
- **El Truco Magistral:** Hacer la línea gruesa (ej. 16pt), con uniones y remates redondeados, pero **ponerle el MISMO color que el fondo de la diapositiva**. Esto crea una ilusión óptica de que el camino "corta" o separa los muros.

### 5. Inserción del "Héroe" (Escala Humana)
- Importar un SVG de una figura humana, convertirlo en forma y desagruparlo.
- **Regla de Escala:** Reducir drásticamente su tamaño (ej. 1.5 cm de alto) para enfatizar la magnitud del entorno y mantener la estética minimalista suiza.

### 6. Animación con Transición Morph (Transformación)
- No usar animaciones tradicionales (aparecer, desvanecer). Todo se controla desde la pestaña `Transiciones > Transformación (Morph)`.
- Duración recomendada: 1.5 segundos (o 1s para pasos más rápidos).

## 📏 Reglas de Oro y Restricciones Críticas (Lógica Morph)
- ⚠️ **La Regla de la Presencia:** Para que Morph funcione, el objeto (la figura humana, los muros) **debe existir en ambas diapositivas** (la actual y la siguiente), solo que en diferentes posiciones.
- ⚠️ **La Regla del Fuera de Pantalla (Fly-in):** Los cuadros de texto que deben "entrar volando" en el paso 2, deben estar presentes en el paso 1, pero **ubicados físicamente fuera del lienzo de la diapositiva** (en el área gris de trabajo). Si solo los copias y pegas en el paso 2, PowerPoint hará un simple "Desvanecer" (Fade) en lugar de animar la entrada.
- **Agrupación:** Agrupar los muros y el camino en un solo objeto para evitar que se desalignen al duplicar diapositivas, dejando a la figura humana y los textos como elementos independientes.

## 💡 Prompts Clave (Para que la IA genere el contenido)
Cuando el usuario quiera usar esta plantilla, deberá pedirle a la IA:
> *"Actúa como un experto en narrativa visual. Tengo una infografía de 4 pasos con estilo suizo minimalista. Dame el texto (título y 2 líneas de descripción) para 4 hitos que hablen sobre [TEMA]. Indícame en qué posición del camino (nodo 1, 2, 3 o 4) debe estar la figura humana en cada slide."*

## 📤 Estructura de Salida (Arquitectura de Slides en PPT)
- **Slide 0 (Base/Backup):** Diseño completo estático. Sirve como respaldo y punto de partida.
- **Slide 1 (Inicio):** Muros + Figura humana en el nodo 1. Textos del paso 1 visibles. Textos del paso 2 *fuera de pantalla a la derecha*.
- **Slide 2 (Paso 2):** Figura humana movida al nodo 2. Textos del paso 2 ahora dentro de pantalla. Textos del paso 3 *fuera de pantalla*.
- **Slide N (Final):** Figura humana en el último nodo. Todos los textos anteriores pueden mantenerse o atenuarse.
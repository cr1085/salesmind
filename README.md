# **LexIA Pro: Asistente de Redacción Jurídica con IA**

**LexIA Pro** representa la siguiente evolución en asistentes legales de IA. Más allá de las simples preguntas y respuestas, esta aplicación funciona como un socio activo en el proceso de redacción legal. Al combinar un potente motor de consulta basado en RAG con un nuevo módulo de generación de documentos basado en plantillas, LexIA Pro puede responder preguntas legales complejas y ayudar en la creación de documentos legales estructurados, como contratos.

Este proyecto es una muestra de un sistema de IA híbrido capaz tanto de recuperar conocimientos como de crear documentos, acelerando significativamente los flujos de trabajo legales.

### ⭐ **Características principales**

-   **Funcionalidad de modo dual:** funciona como **consultor legal** (respondiendo preguntas basadas en su base de conocimientos) y como **redactor asistente** (generando documentos a partir de plantillas).
    
-   **Módulo de Generación de Documentos:** Una nueva funcionalidad que permite a los usuarios seleccionar una plantilla de documento (por ejemplo, un contrato de alquiler) y completarlo a través de un formulario guiado, generando un documento completo y listo para usar.
    
-   **Base de conocimiento de múltiples documentos:** puede indexar y consultar múltiples archivos PDF simultáneamente, creando un "cerebro" legal unificado.
    
-   **IA conversacional con personalidad:** utiliza indicaciones refinadas para responder en un tono natural y didáctico, simulando un verdadero asistente junior.
    
-   **Búsqueda semántica de alta precisión:** emplea un recuperador de compresión contextual para garantizar que solo se utilice la información más relevante para responder preguntas, maximizando la precisión.
    
-   **Cita de la fuente:** Todas las respuestas consultivas están respaldadas por una lista de los documentos fuente utilizados, lo que garantiza la transparencia y la confianza.
    
-   **Motor de inteligencia artificial configurable:** cambie fácilmente entre un modelo local ( **Ollama** ) para privacidad o un modelo en la nube ( **API de Google Gemini** ) para facilitar la implementación.
    

----------

### 🚀 **Demostración de Capacidades**

LexIA Pro puede gestionar una amplia variedad de tareas, desde la consulta hasta la creación:

-   **Consulta:**
    
    -   `"¿Cuáles son los requisitos para que la promesa de celebrar un contrato sea válida según el Código Civil?"`
        
    -   `"Explícame qué es la acción de tutela y en qué casos procede."`
        
-   **Apoyo en la redacción (Extracción de cláusulas):**
    
    -   `"Proporcióname una cláusula de ejemplo sobre el pago del canon mensual para un contrato de arrendamiento."`
        
-   **Generación de documentos:**
    
    -   Vaya a la sección “Borrador de documento”, seleccione “Contrato de alquiler” y complete el formulario para generar un contrato completo.
        

----------

### ⚙️ **Pila tecnológica y configuración**

-   **Backend:** Python, Flask
    
-   **Motor de IA:** Ollama (local) / Google Gemini (nube)
    
-   **Sistema RAG:** LangChain, FAISS, Transformadores de oraciones
    
-   **Base de datos (Usuarios):** SQLite
    
-   **Interfaz:** HTML, CSS, JavaScript


### Instalación y Puesta en Marcha

Sigue estos pasos para ejecutar el proyecto en un entorno local.

#### 1. Prerrequisitos
* Python 3.10+
* (Opcional, para modo local) [Ollama](https://ollama.com/) instalado y ejecutándose.

#### 2. Clonar el Repositorio
```bash
git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
cd tu-repositorio
```

#### 3. Entorno Virtual y Dependencias
```bash
# Crear y activar entorno virtual
python -m venv venv
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

#### 4. Configurar Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto y añade las siguientes variables:

```
# Clave secreta para la seguridad de Flask
SECRET_KEY="una-clave-muy-secreta-y-dificil-de-adivinar"

# Elige el motor de IA. Opciones: "ollama" o "google"
AI_PROVIDER="google"

# Pega tu clave de API si vas a usar el modo 'google'
GOOGLE_API_KEY="AIzaSy...tu_clave_de_google_aqui"
```

#### 5. Crear la Base de Conocimiento
1.  Coloca todos los documentos PDF que el asistente debe estudiar en la carpeta `/biblioteca_pdfs`.
2.  Ejecuta el script indexador **una sola vez**. Este proceso puede tardar varios minutos.
    ```bash
    python indexer.py
    ```

#### 6. Inicializar la Base de Datos de Usuarios
```bash
flask init-db
```

#### 7. Ejecutar la Aplicación
```bash
flask run
```
La aplicación estará disponible en `http://127.0.0.1:5000`.
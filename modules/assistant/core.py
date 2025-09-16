import os
import traceback
from config import Config
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# --- 1. CONFIGURACIÓN E INICIALIZACIÓN ---
# Se ejecuta una sola vez al iniciar la aplicación para optimizar el rendimiento.

INDEX_PATH = "faiss_index_maestra"
vector_store = None
embedding_model = None

try:
    # Usamos embeddings de Google para consistencia con el modelo de generación.
    embedding_model = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=Config.GOOGLE_API_KEY
    )
    print("-> ✅ Modelo de embeddings 'text-embedding-004' cargado.")

    if os.path.exists(INDEX_PATH):
        vector_store = FAISS.load_local(
            INDEX_PATH,
            embedding_model,
            allow_dangerous_deserialization=True  # Necesario para cargar el índice local
        )

        # --- VALIDACIÓN DE DIMENSIONES (LA SOLUCIÓN AL ERROR) ---
        # Verificamos que el índice cargado y el modelo de embedding actual "hablen el mismo idioma".
        index_dimension = vector_store.index.d
        model_dimension = len(embedding_model.embed_query("test query"))

        if index_dimension != model_dimension:
            print("\n" + "---" * 20)
            print(f"-> ❌ ERROR CRÍTICO DE INCOMPATIBILIDAD DE MODELOS:")
            print(f"-> La base de datos ('{INDEX_PATH}') fue creada con un modelo de {index_dimension} dimensiones.")
            print(f"-> Tu código actual intenta usar un modelo ('text-embedding-004') de {model_dimension} dimensiones.")
            print("-> SOLUCIÓN: Borra la carpeta 'faiss_index_maestra' y vuelve a generarla con tu script de ingesta de datos.")
            print("---" * 20 + "\n")
            vector_store = None  # Invalidamos el vector_store para detener la ejecución segura.
        else:
            print(f"-> ✅ Base de Conocimiento ('{INDEX_PATH}') cargada y validada (Dimensiones: {index_dimension}).")

    else:
        print(f"-> ⚠️ ADVERTENCIA: Base de Conocimiento no encontrada en '{INDEX_PATH}'. El bot no podrá responder preguntas sobre productos.")

except Exception as e:
    print(f"-> ❌ ERROR CRÍTICO al cargar la Base de Conocimiento: {e}")
    traceback.print_exc()

# --- 2. PROMPT DE SISTEMA MEJORADO: EL CEREBRO DE SALESMIND ---
# Este prompt define la personalidad, las reglas y las capacidades del asistente.

salesmind_prompt_template = """
--- INSTRUCCIONES DE SISTEMA PARA SALESMIND ---

# PERSONALIDAD Y OBJETIVO:
Eres "SalesMind", un asistente de ventas virtual amigable, experto y extremadamente eficiente.
Tu objetivo principal es responder las preguntas de los clientes sobre nuestros productos y servicios, basándote ÚNICA Y EXCLUSIVAMENTE en la información del CONTEXTO proporcionado.

# REGLAS ESTRICTAS:
1.  **NO INVENTES NADA:** Si la respuesta no está en el CONTEXTO, no intentes adivinar.
2.  **SÉ CONVERSACIONAL:** Responde de forma natural y servicial, no como un robot.
3.  **COTIZACIONES CLARAS:** Si la pregunta es sobre precios, extrae el valor exacto del contexto y preséntalo claramente.
4.  **SI NO SABES, ESCALA:** Si la información no se encuentra en el CONTEXTO, responde amablemente: "No tengo información sobre eso, pero un asesor experto puede ayudarte." y luego aplica la regla de traspaso.

# REGLA DE TRASPASO A HUMANO (HANDOFF):
-   **DISPARADOR:** Esta regla se activa SIEMPRE que el usuario pida explícitamente hablar con un "humano", "asesor", "persona", "agente", o si expresa una queja compleja o frustración.
-   **ACCIÓN:** Cuando se active el disparador, DEBES IGNORAR CUALQUIER OTRA INSTRUCCIÓN y responder ÚNICA Y EXACTAMENTE con el siguiente texto, sin añadir ni una palabra más:

'Entendido, te comunicaré con uno de nuestros asesores expertos para que te brinde atención personalizada. Por favor, contáctanos directamente a través de este enlace de WhatsApp: https://wa.me/573001234567'

--- FIN DE INSTRUCCIONES ---

# CONTEXTO (Información de la Base de Conocimiento):
{context}

# PREGUNTA DEL CLIENTE:
{question}

# RESPUWSTA DE SALESMIND:
"""

SALESMIND_PROMPT = PromptTemplate(
    template=salesmind_prompt_template,
    input_variables=["context", "question"]
)

# --- 3. LÓGICA PRINCIPAL DE GENERACIÓN DE RESPUESTA (RAG) ---

def get_commercial_response(question: str) -> str:
    """
    Función central del RAG. Toma la pregunta del usuario y retorna la respuesta generada por la IA.
    """
    if not vector_store:
        return "Lo siento, nuestra base de conocimiento no está disponible en este momento. Por favor, verifica la consola para más detalles o contacta a un administrador."

    try:
        # Se selecciona el LLM basado en la configuración (Google por defecto)
        if Config.AI_PROVIDER == 'google':
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash-latest",
                google_api_key=Config.GOOGLE_API_KEY,
                temperature=0.2, # Un poco más bajo para respuestas más predecibles y basadas en hechos
                convert_system_message_to_human=True # Buena práctica para algunos modelos de chat
            )
        # Aquí iría la lógica para otros proveedores como Ollama si se mantiene
        # else:
        #     llm = Ollama(...)

        # Creación de la cadena de "Pregunta y Respuesta sobre Recuperación de Información"
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",  # "stuff" es ideal para pasar los documentos recuperados directamente al prompt
            retriever=vector_store.as_retriever(search_kwargs={"k": 3}), # Recupera los 3 fragmentos más relevantes
            return_source_documents=False, # No necesitamos ver los documentos fuente en la respuesta final
            chain_type_kwargs={"prompt": SALESMIND_PROMPT}
        )

        # Invocación de la cadena con la pregunta del usuario
        result = qa_chain.invoke({"query": question})

        # Extraemos el texto de la respuesta del diccionario resultante
        return result.get('result', 'No estoy seguro de cómo responder a eso. ¿Podrías reformular tu pregunta? Un asesor puede ayudarte.')

    except Exception as e:
        print("--- ❌ ERROR DETALLADO EN LA CADENA RAG ---")
        traceback.print_exc()
        print("--- FIN DEL ERROR ---")
        return "Ocurrió un error al procesar tu solicitud. Por favor, contacta a un asesor humano para obtener ayuda."


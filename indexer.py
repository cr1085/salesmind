import os
import fitz
import time
import traceback
from config import Config
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.schema.document import Document

PDFS_PATH = "biblioteca_pdfs/"
INDEX_PATH = "faiss_index_maestra"

def create_master_index():
    print("--- Iniciando Creación de Base de Conocimiento para SalesMind ---")
    if not Config.GOOGLE_API_KEY:
        print("-> ERROR: La GOOGLE_API_KEY no está en tu archivo .env. Proceso detenido.")
        return

    # (El resto del código es tu lógica de lectura de PDFs, que ya funcionaba bien)
    pdf_files = [f for f in os.listdir(PDFS_PATH) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print(f"-> ADVERTENCIA: No se encontraron PDFs en '{PDFS_PATH}'.")
        return
    
    print(f"-> {len(pdf_files)} PDFs encontrados. Procesando...")
    docs_with_metadata = []
    for pdf_file in pdf_files:
        try:
            with fitz.open(os.path.join(PDFS_PATH, pdf_file)) as doc:
                full_text = "".join(page.get_text() for page in doc)
                if full_text.strip():
                    docs_with_metadata.append({"text": full_text, "source": pdf_file})
        except Exception as e:
            print(f"   -> Error leyendo {pdf_file}: {e}")
            continue

    if not docs_with_metadata:
        print("-> ERROR: No se pudo extraer texto de ningún PDF.")
        return

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
    all_chunks = [
        Document(page_content=chunk, metadata={"source": doc["source"]})
        for doc in docs_with_metadata
        for chunk in text_splitter.split_text(doc["text"])
    ]

    print(f"-> {len(all_chunks)} fragmentos de texto creados.")
    print("-> Generando embeddings con Google... (Esto puede tardar)")
    
    try:
        # --- AQUÍ ESTÁ EL CAMBIO CLAVE ---
        # Usamos el mismo modelo y la misma clave que el resto de tu app
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=Config.GOOGLE_API_KEY
        )
        
        vector_store = FAISS.from_documents(all_chunks, embedding=embeddings)
        vector_store.save_local(INDEX_PATH)
        
        print("\n-> ¡ÉXITO! La base de conocimiento se creó correctamente.")
        print(f"-> Índice guardado en '{INDEX_PATH}'.")

    except Exception as e:
        print(f"\n-> ERROR CRÍTICO durante la creación de embeddings: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    create_master_index()
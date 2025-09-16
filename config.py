import os
from dotenv import load_dotenv


# --- LA LÍNEA QUE FALTA ---
# Esta función es la que lee tu archivo .env y carga las claves.
load_dotenv()

# La raíz del proyecto es el directorio donde se encuentra este archivo.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # La base de datos estará en la carpeta 'instance' DENTRO de la raíz del proyecto.
    # Esta es la ruta correcta y robusta.
    DATABASE_PATH = os.path.join(BASE_DIR, 'instance', 'legal_db.db')
    
    # Claves API
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
    
    # El interruptor principal para la IA
    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'ollama')

# Verificación que se imprime en la terminal al iniciar
print("-" * 30)
print(f"-> RUTA DE LA BASE DE DATOS: '{Config.DATABASE_PATH}'")
print(f"-> MODO DE IA CONFIGURADO: '{Config.AI_PROVIDER}'")
print("-" * 30)
# Contenido para: modules/bot/routes.py

from flask import Blueprint, request
from config import Config
import telegram
import sqlite3 # <-- Importamos sqlite3
import asyncio
from modules.assistant.core import get_commercial_response

bot_bp = Blueprint('bot', __name__)
bot = telegram.Bot(token=Config.TELEGRAM_TOKEN)

# --- NUEVA FUNCIÓN PARA GUARDAR MENSAJES ---
def log_message(chat_id, sender, message):
    try:
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO conversations (chat_id, sender, message_text) VALUES (?, ?, ?)",
            (chat_id, sender, message)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error al guardar el mensaje en la base de datos: {e}")
# --- FIN DE LA NUEVA FUNCIÓN ---

def run_async(coro):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

@bot_bp.route('/telegram_webhook', methods=['POST'])
def telegram_webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    if update.message and update.message.text:
        chat_id = update.message.chat.id
        user_message = update.message.text

        # --- AÑADIMOS EL REGISTRO DE MENSAJES ---
        # 1. Guardamos el mensaje del usuario
        log_message(chat_id, 'user', user_message)

        # 2. Obtenemos la respuesta de la IA
        ai_message = get_commercial_response(user_message)

        # 3. Guardamos la respuesta del bot
        log_message(chat_id, 'bot', ai_message)
        # --- FIN DEL REGISTRO ---

        run_async(bot.send_message(chat_id=chat_id, text=ai_message))

    return "OK", 200
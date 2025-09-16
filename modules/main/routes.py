import sqlite3
from config import Config
from collections import defaultdict
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)


@main_bp.route('/manual')
@login_required
def manual():
    return render_template('manual.html')


@main_bp.route('/conversations')
@login_required
def conversations_dashboard():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Obtenemos todos los mensajes ordenados por fecha
    cursor.execute("SELECT * FROM conversations ORDER BY timestamp ASC")
    messages = cursor.fetchall()
    conn.close()
    
    # Agrupamos los mensajes por chat_id para separar las conversaciones
    conversations = defaultdict(list)
    for msg in messages:
        conversations[msg['chat_id']].append(dict(msg))
        
    return render_template('conversations_dashboard.html', conversations=conversations)
# --- FIN DE LA NUEVA RUTA ---
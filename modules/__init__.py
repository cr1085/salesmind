# from flask import Flask
# from flask_login import LoginManager
# import os
# import click
# from .auth.models import User, init_db
# from config import Config
# from .assistant.rag_processor import RAGProcessor

# def create_app():
#     app = Flask(__name__, instance_relative_config=True)
    
#     app.config.from_object(Config)
    
#     app.secret_key = app.config.get('SECRET_KEY', 'dev-key-shhh-this-is-secret')
    
#     app.rag_processor = RAGProcessor()

#     login_manager = LoginManager()
#     login_manager.login_view = 'auth.login'
#     login_manager.init_app(app)

#     @login_manager.user_loader
#     def load_user(user_id):
#         return User.get(user_id)

#     # Registrar Blueprints
#     from .auth.routes import auth_bp
#     app.register_blueprint(auth_bp)

#     from .main.routes import main_bp
#     app.register_blueprint(main_bp)

#     from .assistant.routes import assistant_bp
#     app.register_blueprint(assistant_bp)
    
#     from .documents.routes import documents_bp
#     app.register_blueprint(documents_bp)
    
#     # --- CAMBIO AQUÍ: Registramos el nuevo blueprint de admin ---
#     from .admin.routes import admin_bp
#     app.register_blueprint(admin_bp)
#     # --- FIN DEL CAMBIO ---

#     # --- AÑADIR ESTAS LÍNEAS ---
#     from .drafting.routes import drafting_bp
#     app.register_blueprint(drafting_bp)
#     # --- FIN ---
#     from .bot.routes import bot_bp
#     app.register_blueprint(bot_bp)
    
#     @app.cli.command('init-db')
#     def init_db_command():
#         init_db()
#         click.echo('Base de datos inicializada.')

#     return app



# /modules/__init__.py

from flask import Flask
from flask_login import LoginManager
import os
import click
from .auth.models import User, init_db
from config import Config
from .assistant.rag_processor import RAGProcessor

def create_app():
    """
    Esta es la fábrica de aplicaciones LIGERA Y CORRECTA para SalesMind.
    """
    # 1. Creamos la instancia de la aplicación
    app = Flask(__name__)

    # 2. Cargamos la configuración desde nuestro archivo config.py
    app.config.from_object(Config)

    # 3. Importamos y registramos ÚNICAMENTE el blueprint que necesitamos:
    #    el que contiene nuestro webhook de WhatsApp.
    from .assistant.routes import assistant_bp
    app.register_blueprint(assistant_bp)

    # 4. (Opcional) Una ruta para verificar que el servidor está en línea
    @app.route("/")
    def index():
        return "¡El servidor de SalesMind está en línea y funcionando correctamente!"

    return app
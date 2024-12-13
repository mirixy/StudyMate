from flask import Flask
from .extensions import db, login_manager
from flask_migrate import Migrate  # Import Flask-Migrate
from .models import User  # Importiere das User-Modell später, um den Zirkularimport zu vermeiden.
from flask_wtf.csrf import CSRFProtect

migrate = Migrate()  # Initialize Flask-Migrate

@login_manager.user_loader
def load_user(user_id):
    """Lädt den Benutzer aus der Datenbank anhand der user_id."""
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object("config.Config")
    csrf = CSRFProtect(app)  # Initialize CSRF protection
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "main.login"  # Weiterleitung zur Login-Seite
    
    migrate.init_app(app, db)  # Initialize Flask-Migrate with the app and db

    from .routes import main
    app.register_blueprint(main)
    
    return app
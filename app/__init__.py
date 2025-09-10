# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager # Add this import
from config import Config

db = SQLAlchemy()
login_manager = LoginManager() # Add this line
login_manager.login_view = 'main.login' # Add this line, redirects non-logged-in users

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app) # Add this line

    from app.routes import main
    app.register_blueprint(main)

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app
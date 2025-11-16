
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import config_by_name
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):

    app = Flask(__name__, instance_relative_config=True)


    config_name_to_use = os.getenv('FLASK_ENV', config_name)
    app.config.from_object(config_by_name[config_name_to_use])

    db.init_app(app)
    migrate.init_app(app, db)

    # --- Реєстрація Blueprint (поки закоментовано) ---
    # Ми розкоментуємо це в Частині 2, коли створимо 'posts_bp'
    # from app.posts import posts_bp
    # app.register_blueprint(posts_bp, url_prefix='/post')
    # --- Кінець Blueprint ---

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404


    @app.route('/')
    def home():

        return "Фабрика додатків працює! Ми ще не створили Blueprint 'posts'."

    return app
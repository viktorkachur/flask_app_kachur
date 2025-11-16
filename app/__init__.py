from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import config_by_name
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from app.posts import post_bp
    from app.posts import views
    app.register_blueprint(post_bp, url_prefix='/post')

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.route('/')
    def home():
        return redirect(url_for('posts.all_posts'))

    return app
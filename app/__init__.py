from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from app.config import config_by_name
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
import os

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=naming_convention)


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app(config_name='default'):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.posts import post_bp
    from app.posts import views
    app.register_blueprint(post_bp, url_prefix='/post')

    from app.products import products_bp
    from app.products.models import Product
    app.register_blueprint(products_bp, url_prefix='/products')

    from app.users import users_bp
    app.register_blueprint(users_bp, url_prefix='/users')

    from app.models import User

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.route('/')
    def home():
        return redirect(url_for('posts.all_posts'))

    return app
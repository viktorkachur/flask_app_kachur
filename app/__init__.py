
from flask import Flask


application = Flask(__name__)

application.config.from_object('config.AppConfig')
from app.users import users_bp

application.register_blueprint(users_bp, url_prefix='/users')

from app import views
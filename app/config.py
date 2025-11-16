import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-fallback-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    INSTANCE_PATH = os.path.join(basedir, 'instance')

    os.makedirs(INSTANCE_PATH, exist_ok=True)



class DevelopmentConfig(Config):
    DEBUG = True
    # 3. Беремо назву файлу з .env
    DB_NAME = os.environ.get('DATABASE_FILE') or 'dev.sqlite'
    # 4. ЗАВЖДИ будуємо АБСОЛЮТНИЙ шлях
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Config.INSTANCE_PATH, DB_NAME)


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False
    DB_NAME = os.environ.get('DATABASE_FILE') or 'data.sqlite'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Config.INSTANCE_PATH, DB_NAME)


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
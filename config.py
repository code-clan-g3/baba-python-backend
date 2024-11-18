import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    WTF_CSRF_ENABLED = False


class ProdConfig(Config):
    DEBUG = False

class DevConfig(Config):
    DEBUG = True
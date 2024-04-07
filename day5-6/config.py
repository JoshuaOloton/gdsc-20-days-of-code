import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.db')

class ProductionConfig(Config):
    pass


config = {
    'default': DevelopmentConfig,
}
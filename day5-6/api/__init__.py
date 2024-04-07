from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import config

db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .books import books as books_blueprint
    app.register_blueprint(books_blueprint, url_prefix='/api')


    return app
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import config

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/v1')

    from .books import books as books_blueprint
    app.register_blueprint(books_blueprint, url_prefix='/api/v1')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .users import users as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/api/v1')


    return app
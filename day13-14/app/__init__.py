from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import config

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_name='default'):
    app = Flask(__name__, template_folder='api/templates')
    app.config.from_object(config[config_name])

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from .api.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/v1')

    from .api.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/api/v1')

    from .api.books import books as books_blueprint
    app.register_blueprint(books_blueprint, url_prefix='/api/v1')

    from .api.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api.users import users as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/api/v1')

    from .web import web as web_blueprint
    app.register_blueprint(web_blueprint)


    return app
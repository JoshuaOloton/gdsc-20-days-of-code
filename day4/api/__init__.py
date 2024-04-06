from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import config
import os

db = SQLAlchemy()

def create_app(config_name='default'):
  app = Flask(__name__)
  app.config.from_object(config[config_name])

  db.init_app(app)

  return app
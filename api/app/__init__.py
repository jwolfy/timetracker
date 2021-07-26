import logging

from flask import Flask
from app.api.models import db
from app.api import api
from config import Config


logging.basicConfig(level=Config.LOG_LEVEL)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    app.register_blueprint(api)

    return app

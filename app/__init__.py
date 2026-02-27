from flask import Flask
from app.api import register_blueprints

from flask import Flask
from app.api import register_blueprints


def create_app(config_name="development"):
    app = Flask(__name__)

    register_blueprints(app)

    return app
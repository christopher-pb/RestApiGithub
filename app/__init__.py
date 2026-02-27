from flask import Flask
from app.api import register_blueprints


def create_app(config_name="development"):
    """
    Application factory
    Accepts config_name for testing, development, production
    """

    app = Flask(__name__)

    # Optional config (needed for GitHub Actions tests)
    app.config["TESTING"] = config_name == "testing"

    register_blueprints(app)

    return app
from flask import Flask
from app.extensions import jwt
from app.config import config_by_name


def create_app(config_name: str = "development") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    jwt.init_app(app)

    from app.api.auth import auth_bp
    from app.api.students import students_bp
    from app.api.health import health_bp

    app.register_blueprint(health_bp, url_prefix="/api/v1")
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(students_bp, url_prefix="/api/v1/students")  
    from app.errors import register_error_handlers
    register_error_handlers(app)

    return app
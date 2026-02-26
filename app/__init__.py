"""
Flask REST API Application Factory.
"""
from flask import Flask
from app.extensions import jwt
from app.config import config_by_name


def create_app(config_name: str = "development") -> Flask:
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    jwt.init_app(app)

    # Register blueprints
    from app.api.auth import auth_bp
    from app.api.students import students_bp
    from app.api.health import health_bp
    from app.api.employees import employees_bp
    from app.api.departments import departments_bp
    from app.api.salaries import salaries_bp

    app.register_blueprint(health_bp, url_prefix="/api/v1")
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(students_bp, url_prefix="/api/v1/students")
    app.register_blueprint(employees_bp, url_prefix="/api/v1/employees")
    app.register_blueprint(departments_bp, url_prefix="/api/v1/departments")
    app.register_blueprint(salaries_bp, url_prefix="/api/v1/salaries")

    # Register error handlers
    from app.errors import register_error_handlers
    register_error_handlers(app)

    return app
from app.api.health import health_bp
from app.api.employee import employee_bp
from app.api.department import department_bp
from app.api.salary import salary_bp
from app.api.auth import auth_bp


def register_blueprints(app):
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(employee_bp, url_prefix="/employees")
    app.register_blueprint(department_bp, url_prefix="/departments")
    app.register_blueprint(salary_bp, url_prefix="/salaries")
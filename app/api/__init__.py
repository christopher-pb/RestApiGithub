from app.api.employee import employee_bp
from app.api.department import department_bp
from app.api.salary import salary_bp
from app.api.health import health_bp


def register_blueprints(app):

    app.register_blueprint(employee_bp)
    app.register_blueprint(department_bp)
    app.register_blueprint(salary_bp)
    app.register_blueprint(health_bp)
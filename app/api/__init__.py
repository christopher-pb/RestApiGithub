from flask import Blueprint

api_bp = Blueprint("api", __name__)

from app.api.auth import auth_bp
from app.api.health import health_bp
from app.api.students import students_bp
from app.api.employee import employee_bp

api_bp.register_blueprint(auth_bp, url_prefix="/auth")
api_bp.register_blueprint(health_bp, url_prefix="/health")
api_bp.register_blueprint(students_bp, url_prefix="/students")
api_bp.register_blueprint(employee_bp, url_prefix="/employees")
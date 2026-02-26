from flask import Blueprint

api_bp = Blueprint("api", __name__)

from .employees import employees_bp

api_bp.register_blueprint(employees_bp, url_prefix="/employees")

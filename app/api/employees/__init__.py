from flask import Blueprint

employees_bp = Blueprint("employees", __name__)

from . import routes

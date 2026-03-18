from flask import Flask
from app.api.employee import employee_bp  # singular, matches employee.py

def create_app():
    app = Flask(__name__)
    app.register_blueprint(employee_bp, url_prefix="/api")
    return app
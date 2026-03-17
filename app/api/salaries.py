"""
Salaries blueprint – full CRUD for salaries.
"""

import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required

from app.models.salary import Salary
from app.repositories.json_repository import JsonRepository
from app.services.salary_service import SalaryService

salaries_bp = Blueprint("salaries", __name__)


def _get_service() -> SalaryService:
    data_dir = current_app.config["DATA_DIR"]
    repo = JsonRepository[Salary](os.path.join(data_dir, "salaries.json"), Salary)
    return SalaryService(repo)


@salaries_bp.route("", methods=["GET"])
@jwt_required()
def list_salaries():
    salaries = _get_service().list_salaries()
    return jsonify({"count": len(salaries), "salaries": salaries}), 200


@salaries_bp.route("/<int:salary_id>", methods=["GET"])
@jwt_required()
def get_salary(salary_id: int):
    salary = _get_service().get_salary(salary_id)

    if salary is None:
        return jsonify({"error": "Salary not found"}), 404

    return jsonify(salary), 200


@salaries_bp.route("", methods=["POST"])
@jwt_required()
def create_salary():
    body = request.get_json(silent=True) or {}

    required = ("salaryID", "employeeID", "basicSalary", "bonus", "allowances")
    missing = [f for f in required if f not in body]

    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    try:
        salary = _get_service().create_salary(body)
        return jsonify({"message": "Salary created", "salary": salary}), 201

    except ValueError as exc:
        return jsonify({"error": str(exc)}), 409
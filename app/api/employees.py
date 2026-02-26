import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from app.models.employee import Employee
from app.repositories.json_repository import JsonRepository
from app.services.employee_service import EmployeeService

employees_bp = Blueprint("employees", __name__)


def _get_service() -> EmployeeService:
    data_dir = current_app.config["DATA_DIR"]
    repo = JsonRepository[Employee](os.path.join(data_dir, "employees.json"), Employee)
    return EmployeeService(repo)


@employees_bp.route("", methods=["GET"])
@jwt_required()
def list_employees():
    employees = _get_service().list_employees()
    return jsonify({"count": len(employees), "employees": employees}), 200


@employees_bp.route("/<string:employee_id>", methods=["GET"])
@jwt_required()
def get_employee(employee_id: str):
    emp = _get_service().get_employee(employee_id)
    if emp is None:
        return jsonify({"error": "Employee not found"}), 404
    return jsonify(emp), 200


@employees_bp.route("", methods=["POST"])
@jwt_required()
def create_employee():
    body = request.get_json(silent=True) or {}
    required = ("first_name", "last_name", "gender", "date_of_birth", "department_id")
    missing = [f for f in required if not body.get(f, "").strip()]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    emp = _get_service().create_employee(body)
    return jsonify({"message": "Employee created", "employee": emp}), 201


@employees_bp.route("/<string:employee_id>", methods=["PUT"])
@jwt_required()
def update_employee(employee_id: str):
    body = request.get_json(silent=True) or {}
    result = _get_service().update_employee(employee_id, body)
    if result is None:
        return jsonify({"error": "Employee not found"}), 404
    return jsonify({"message": "Employee updated", "employee": result}), 200


@employees_bp.route("/<string:employee_id>", methods=["DELETE"])
@jwt_required()
def delete_employee(employee_id: str):
    if _get_service().delete_employee(employee_id):
        return jsonify({"message": "Employee deleted"}), 200
    return jsonify({"error": "Employee not found"}), 404
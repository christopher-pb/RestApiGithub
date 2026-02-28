from flask import Blueprint, request, jsonify
from app.services.employee_service import EmployeeService

employees_bp = Blueprint("employees", __name__)

@employees_bp.route("/", methods=["GET"])
def get_employees():
    return jsonify(EmployeeService.get_all())

@employees_bp.route("/<int:emp_id>", methods=["GET"])
def get_employee(emp_id):
    emp = EmployeeService.get_by_id(emp_id)
    if not emp:
        return jsonify({"error": "Employee not found"}), 404
    return jsonify(emp)

@employees_bp.route("/", methods=["POST"])
def add_employee():
    data = request.json
    return jsonify(EmployeeService.add(data)), 201

@employees_bp.route("/<int:emp_id>", methods=["PUT"])
def update_employee(emp_id):
    data = request.json
    emp = EmployeeService.update(emp_id, data)
    if not emp:
        return jsonify({"error": "Employee not found"}), 404
    return jsonify(emp)

@employees_bp.route("/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    EmployeeService.delete(emp_id)
    return jsonify({"message": "Employee deleted successfully"})
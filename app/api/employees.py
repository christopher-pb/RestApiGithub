from flask import Blueprint, request, jsonify
from app.repositories.json_repository import JsonRepository
from app.models.employees import Employee

employees_bp = Blueprint("employees", __name__)
repo = JsonRepository("data/employee.json", Employee)

@employees_bp.get("")
def get_all():
    employees = repo.get_all()
    return jsonify([e.to_dict() for e in employees])

@employees_bp.post("")
def create():
    data = request.json
    emp = Employee.from_dict(data)
    repo.create(emp)
    return emp.to_dict(), 201

@employees_bp.get("/<string:emp_id>")
def get_by_id(emp_id):
    emp = repo.get_by_id(emp_id)
    if not emp:
        return jsonify({"error": "Employee not found"}), 404
    return jsonify(emp.to_dict())

@employees_bp.delete("/<string:emp_id>")
def delete(emp_id):
    deleted = repo.delete(emp_id)

    if not deleted:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify({"message": "Employee deleted"})

@employees_bp.put("/<string:emp_id>")
def update(emp_id):
    data = request.json
    emp = Employee.from_dict(data)

    updated = repo.update(emp_id, emp)

    if not updated:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify(updated.to_dict())
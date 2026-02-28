from flask import Blueprint, request, jsonify
from app.repositories.json_repository import JsonRepository
from app.models.department import Department

department_bp = Blueprint("department", __name__)

repo = JsonRepository("data/department.json", Department)

@department_bp.get("")
def get_all():
    departments = repo.get_all()
    return jsonify([d.to_dict() for d in departments])

@department_bp.post("")
def create():
    data = request.json
    dept = Department.from_dict(data)
    repo.create(dept)
    return dept.to_dict(), 201

@department_bp.get("/<string:dept_id>")
def get_by_id(dept_id):
    dept = repo.get_by_id(dept_id)

    if not dept:
        return jsonify({"error": "Department not found"}), 404

    return jsonify(dept.to_dict())

@department_bp.put("/<string:dept_id>")
def update(dept_id):
    data = request.json
    dept = Department.from_dict(data)

    updated = repo.update(dept_id, dept)

    if not updated:
        return jsonify({"error": "Department not found"}), 404

    return jsonify(updated.to_dict())

@department_bp.delete("/<string:dept_id>")
def delete(dept_id):
    deleted = repo.delete(dept_id)

    if not deleted:
        return jsonify({"error": "Department not found"}), 404

    return jsonify({"message": "Department deleted"})
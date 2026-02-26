from flask import Blueprint, request, jsonify
from app.services.department_service import DepartmentService

departments_bp = Blueprint("departments", __name__)


@departments_bp.route("/", methods=["POST"])
def create_department():
    service = DepartmentService()
    try:
        data = request.get_json()
        department = service.create_department(data)
        return jsonify({
            "message": "Department created",
            "department": department
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@departments_bp.route("/", methods=["GET"])
def get_all_departments():
    service = DepartmentService()
    return jsonify(service.get_all_departments()), 200


@departments_bp.route("/<department_id>", methods=["GET"])
def get_department(department_id):
    service = DepartmentService()
    department = service.get_department_by_id(department_id)
    if not department:
        return jsonify({"error": "Department not found"}), 404
    return jsonify(department), 200


@departments_bp.route("/<department_id>", methods=["PUT"])
def update_department(department_id):
    service = DepartmentService()
    data = request.get_json()
    updated = service.update_department(department_id, data)
    if not updated:
        return jsonify({"error": "Department not found"}), 404
    return jsonify({
        "message": "Department updated",
        "department": updated
    }), 200


@departments_bp.route("/<department_id>", methods=["DELETE"])
def delete_department(department_id):
    service = DepartmentService()
    deleted = service.delete_department(department_id)
    if not deleted:
        return jsonify({"error": "Department not found"}), 404
    return jsonify({"message": "Department deleted"}), 200
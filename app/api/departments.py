"""
Departments blueprint – full CRUD for departments.
"""

import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required

from app.models.department import Department
from app.repositories.json_repository import JsonRepository
from app.services.department_service import DepartmentService

departments_bp = Blueprint("departments", __name__)


def _get_service() -> DepartmentService:
    data_dir = current_app.config["DATA_DIR"]
    repo = JsonRepository[Department](os.path.join(data_dir, "departments.json"), Department)
    return DepartmentService(repo)


@departments_bp.route("", methods=["GET"])
@jwt_required()
def list_departments():
    departments = _get_service().list_departments()
    return jsonify({"count": len(departments), "departments": departments}), 200


@departments_bp.route("/<int:department_id>", methods=["GET"])
@jwt_required()
def get_department(department_id: int):
    department = _get_service().get_department(department_id)

    if department is None:
        return jsonify({"error": "Department not found"}), 404

    return jsonify(department), 200


@departments_bp.route("", methods=["POST"])
@jwt_required()
def create_department():
    body = request.get_json(silent=True) or {}

    required = ("departmentID", "departmentName", "location")
    missing = [f for f in required if not body.get(f)]

    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    try:
        department = _get_service().create_department(body)
        return jsonify({"message": "Department created", "department": department}), 201

    except ValueError as exc:
        return jsonify({"error": str(exc)}), 409
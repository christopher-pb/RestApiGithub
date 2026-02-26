import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from app.models.department import Department
from app.repositories.json_repository import JsonRepository
from app.services.department_service import DepartmentService

departments_bp = Blueprint("departments", __name__, url_prefix="/api/v1/departments")

def _get_service() -> DepartmentService:
    """Helper to get configured department service"""
    data_dir = current_app.config["DATA_DIR"]
    repo = JsonRepository[Department](os.path.join(data_dir, "departments.json"), Department)
    return DepartmentService(repo)

@departments_bp.route("", methods=["GET"])
@jwt_required()
def list_departments():
    """List all departments"""
    departments = _get_service().list_departments()
    return jsonify({"count": len(departments), "departments": departments}), 200

@departments_bp.route("/<string:department_id>", methods=["GET"])
@jwt_required()
def get_department(department_id: str):
    """Get a single department by ID"""
    department = _get_service().get_department(department_id)
    if department is None:
        return jsonify({"error": "Department not found"}), 404
    return jsonify(department), 200

@departments_bp.route("", methods=["POST"])
@jwt_required()
def create_department():
    """Create a new department"""
    body = request.get_json(silent=True) or {}
    
    # Check required fields
    required_fields = ["departmentName", "location"]
    missing = [f for f in required_fields if not body.get(f, "").strip()]
    
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400
    
    try:
        department = _get_service().create_department(body)
        return jsonify(department), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 409

@departments_bp.route("/<string:department_id>", methods=["PUT"])
@jwt_required()
def update_department(department_id: str):
    """Update an existing department"""
    body = request.get_json(silent=True) or {}
    
    result = _get_service().update_department(department_id, body)
    if result is None:
        return jsonify({"error": "Department not found"}), 404
    
    return jsonify({"message": "Department updated", "department": result}), 200

@departments_bp.route("/<string:department_id>", methods=["DELETE"])
@jwt_required()
def delete_department(department_id: str):
    """Delete a department"""
    if _get_service().delete_department(department_id):
        return jsonify({"message": "Department deleted"}), 200
    return jsonify({"error": "Department not found"}), 404
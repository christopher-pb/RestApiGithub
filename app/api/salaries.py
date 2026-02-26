import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from app.models.salary import Salary
from app.repositories.json_repository import JsonRepository
from app.services.salary_service import SalaryService

salaries_bp = Blueprint("salaries", __name__, url_prefix="/api/v1/salaries")

def _get_service() -> SalaryService:
    """Helper to get configured salary service"""
    data_dir = current_app.config["DATA_DIR"]
    repo = JsonRepository[Salary](os.path.join(data_dir, "salaries.json"), Salary)
    return SalaryService(repo)

@salaries_bp.route("", methods=["GET"])
@jwt_required()
def list_salaries():
    """List all salaries"""
    salaries = _get_service().list_salaries()
    return jsonify({"count": len(salaries), "salaries": salaries}), 200

@salaries_bp.route("/<string:salary_id>", methods=["GET"])
@jwt_required()
def get_salary(salary_id: str):
    """Get a single salary by ID"""
    salary = _get_service().get_salary(salary_id)
    if salary is None:
        return jsonify({"error": "Salary not found"}), 404
    return jsonify(salary), 200

@salaries_bp.route("/employee/<string:employee_id>", methods=["GET"])
@jwt_required()
def get_salaries_by_employee(employee_id: str):
    """Get all salaries for a specific employee"""
    try:
        salaries = _get_service().get_salaries_by_employee(employee_id)
        return jsonify({"count": len(salaries), "salaries": salaries}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@salaries_bp.route("", methods=["POST"])
@jwt_required()
def create_salary():
    """Create a new salary record"""
    body = request.get_json(silent=True) or {}
    
    # Check required fields
    required_fields = ["employeeId", "basicSalary", "bonus", "allowances"]
    missing = []
    
    for field in required_fields:
        if field not in body or body[field] is None:
            missing.append(field)
        elif field == "employeeId" and not str(body[field]).strip():
            missing.append(field)
    
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400
    
    # Validate numeric fields
    try:
        body["basicSalary"] = float(body["basicSalary"])
        body["bonus"] = float(body["bonus"])
        body["allowances"] = float(body["allowances"])
    except (ValueError, TypeError):
        return jsonify({"error": "Salary, bonus, and allowances must be valid numbers"}), 400
    
    try:
        salary = _get_service().create_salary(body)
        return jsonify(salary), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@salaries_bp.route("/<string:salary_id>", methods=["PUT"])
@jwt_required()
def update_salary(salary_id: str):
    """Update an existing salary record"""
    body = request.get_json(silent=True) or {}
    
    # Validate numeric fields if present
    for field in ["basicSalary", "bonus", "allowances"]:
        if field in body:
            try:
                body[field] = float(body[field])
            except (ValueError, TypeError):
                return jsonify({"error": f"{field} must be a valid number"}), 400
    
    try:
        result = _get_service().update_salary(salary_id, body)
        if result is None:
            return jsonify({"error": "Salary not found"}), 404
        return jsonify({"message": "Salary updated", "salary": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@salaries_bp.route("/<string:salary_id>", methods=["DELETE"])
@jwt_required()
def delete_salary(salary_id: str):
    """Delete a salary record"""
    try:
        if _get_service().delete_salary(salary_id):
            return jsonify({"message": "Salary deleted"}), 200
        return jsonify({"error": "Salary not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
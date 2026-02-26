import os
from flask import Blueprint, request, jsonify, current_app
from app.models.salary import Salary
from app.models.employee import Employee
from app.repositories.json_repository import JsonRepository
from app.services.salary_service import SalaryService


salary_bp = Blueprint("salary", __name__)


def get_service():

    data_dir = current_app.config["DATA_DIR"]

    salary_repo = JsonRepository(
        os.path.join(data_dir, "salaries.json"),
        Salary,
    )

    employee_repo = JsonRepository(
        os.path.join(data_dir, "employees.json"),
        Employee,
    )

    return SalaryService(salary_repo, employee_repo)


# ----------------------------
# CREATE
# ----------------------------
@salary_bp.route("/", methods=["POST"])
def create_salary():
    service = get_service()

    try:
        result = service.create_salary(request.json)
        return jsonify({
            "message": "Salary created",
            "salary": result
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# ----------------------------
# LIST
# ----------------------------
@salary_bp.route("/", methods=["GET"])
def list_salaries():
    service = get_service()
    return jsonify(service.list_salaries())


# ----------------------------
# GET
# ----------------------------
@salary_bp.route("/<salary_id>", methods=["GET"])
def get_salary(salary_id):
    service = get_service()
    salary = service.get_salary(salary_id)

    if not salary:
        return jsonify({"error": "Salary not found"}), 404

    return jsonify(salary)


# ----------------------------
# UPDATE
# ----------------------------
@salary_bp.route("/<salary_id>", methods=["PUT"])
def update_salary(salary_id):
    service = get_service()
    salary = service.update_salary(salary_id, request.json)

    if not salary:
        return jsonify({"error": "Salary not found"}), 404

    return jsonify({
        "message": "Salary updated",
        "salary": salary
    })


# ----------------------------
# DELETE
# ----------------------------
@salary_bp.route("/<salary_id>", methods=["DELETE"])
def delete_salary(salary_id):
    service = get_service()
    success = service.delete_salary(salary_id)

    if not success:
        return jsonify({"error": "Salary not found"}), 404

    return jsonify({"message": "Salary deleted"})
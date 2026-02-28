from flask import Blueprint, request, jsonify
from app.repositories.json_repository import JsonRepository
from app.models.salaries import Salary

salaries_bp = Blueprint("salaries", __name__)

repo = JsonRepository("data/salaries.json", Salary)


# GET ALL
@salaries_bp.get("")
def get_all():
    salaries = repo.get_all()
    return jsonify([s.to_dict() for s in salaries])


# GET BY ID
@salaries_bp.get("/<string:salary_id>")
def get_by_id(salary_id):
    sal = repo.get_by_id(salary_id)

    if not sal:
        return jsonify({"error": "Salary not found"}), 404

    return jsonify(sal.to_dict())


# CREATE
@salaries_bp.post("")
def create():
    data = request.json
    sal = Salary.from_dict(data)
    repo.create(sal)
    return jsonify(sal.to_dict()), 201


# UPDATE
@salaries_bp.put("/<string:salary_id>")
def update(salary_id):
    data = request.json
    sal = Salary.from_dict(data)

    updated = repo.update(salary_id, sal)

    if not updated:
        return jsonify({"error": "Salary not found"}), 404

    return jsonify(updated.to_dict())


# DELETE
@salaries_bp.delete("/<string:salary_id>")
def delete(salary_id):
    deleted = repo.delete(salary_id)

    if not deleted:
        return jsonify({"error": "Salary not found"}), 404

    return jsonify({"message": "Salary deleted"})
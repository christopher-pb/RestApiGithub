from flask import Blueprint, jsonify, request

employees_bp = Blueprint("employees_bp", __name__)

# Sample data (temporary like student example)
employees = [
    {"id": 1, "name": "Akshaya", "role": "Developer"},
    {"id": 2, "name": "Rahul", "role": "Tester"}
]

# GET all employees
@employees_bp.route("/", methods=["GET"])
def get_employees():
    return jsonify(employees), 200


# GET employee by id
@employees_bp.route("/<int:id>", methods=["GET"])
def get_employee(id):
    for emp in employees:
        if emp["id"] == id:
            return jsonify(emp), 200
    return jsonify({"message": "Employee not found"}), 404


# POST create employee
@employees_bp.route("/", methods=["POST"])
def create_employee():
    data = request.get_json()
    new_employee = {
        "id": len(employees) + 1,
        "name": data.get("name"),
        "role": data.get("role")
    }
    employees.append(new_employee)
    return jsonify(new_employee), 201

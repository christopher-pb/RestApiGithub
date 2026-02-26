from flask import Blueprint, jsonify

employee_bp = Blueprint('employee_bp', __name__)

@employee_bp.route('/employees', methods=['GET'])
def get_employees():
    employees = [
        {"id": 1, "name": "Akshaya", "role": "Developer"},
        {"id": 2, "name": "Rahul", "role": "Tester"},
        {"id": 3, "name": "Sneha", "role": "Manager"}
    ]
    return jsonify(employees)

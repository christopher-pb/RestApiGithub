import json
from flask import Blueprint, request, jsonify

# ✅ DEFINE FIRST
employees_bp = Blueprint('employees', __name__)

DATA_FILE = 'data/employees.json'

def read_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# ✅ GET all
@employees_bp.route('/', methods=['GET'])
def get_employees():
    return jsonify(read_data())

# ✅ GET one
@employees_bp.route('/<int:id>', methods=['GET'])
def get_employee(id):
    employees = read_data()
    emp = next((e for e in employees if e['EmployeeID'] == id), None)
    if emp:
        return jsonify(emp)
    return {"message": "Employee not found"}, 404

# ✅ POST
@employees_bp.route('/', methods=['POST'])
def add_employee():
    employees = read_data()
    new_emp = request.json
    employees.append(new_emp)
    write_data(employees)
    return jsonify(new_emp), 201

# ✅ PUT
@employees_bp.route('/<int:id>', methods=['PUT'])
def update_employee(id):
    employees = read_data()
    for emp in employees:
        if emp['EmployeeID'] == id:
            emp.update(request.json)
            write_data(employees)
            return jsonify(emp)
    return {"message": "Employee not found"}, 404

# ✅ DELETE
@employees_bp.route('/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employees = read_data()
    employees = [e for e in employees if e['EmployeeID'] != id]
    write_data(employees)
    return {"message": "Deleted"}
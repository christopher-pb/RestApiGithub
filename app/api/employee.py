from flask import Blueprint, jsonify, request
import json

employee_bp = Blueprint("employee", __name__)

FILE = "data/employees.json"


def read_data():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []


def write_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


@employee_bp.route("/employees", methods=["GET"])
def get_employees():
    return jsonify(read_data())


@employee_bp.route("/employees", methods=["POST"])
def add_employee():
    employees = read_data()
    new_employee = request.json
    employees.append(new_employee)
    write_data(employees)
    return jsonify(new_employee), 201
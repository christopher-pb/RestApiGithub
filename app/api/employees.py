from flask import Blueprint, request, jsonify, current_app
import os
import json

employees_bp = Blueprint("employees", __name__)

def get_data_file():
    return os.path.join(current_app.config["DATA_DIR"], "employees.json")

def load_employees():
    with open(get_data_file(), "r") as f:
        return json.load(f)

def save_employees(data):
    with open(get_data_file(), "w") as f:
        json.dump(data, f, indent=4)

@employees_bp.route("", methods=["GET"])
def get_all_employees():
    return jsonify(load_employees()), 200

@employees_bp.route("", methods=["POST"])
def create_employee():
    data = request.get_json()
    employees = load_employees()
    employees.append(data)
    save_employees(employees)
    return jsonify({"message": "Employee added"}), 201
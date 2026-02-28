from flask import Blueprint, request, jsonify
import json
import os

employees_bp = Blueprint("employees_bp", __name__)

DATA_FILE = os.path.join("data", "employees.json")


def read_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def write_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


@employees_bp.route("/", methods=["GET"])
def get_employees():
    return jsonify(read_data())


@employees_bp.route("/<int:id>", methods=["GET"])
def get_employee(id):
    employees = read_data()
    for emp in employees:
        if emp["EmployeeID"] == id:
            return jsonify(emp)
    return jsonify({"message": "Employee not found"}), 404


@employees_bp.route("/", methods=["POST"])
def add_employee():
    employees = read_data()
    new_employee = request.json
    employees.append(new_employee)
    write_data(employees)
    return jsonify(new_employee), 201


@employees_bp.route("/<int:id>", methods=["PUT"])
def update_employee(id):
    employees = read_data()
    for emp in employees:
        if emp["EmployeeID"] == id:
            emp.update(request.json)
            write_data(employees)
            return jsonify(emp)
    return jsonify({"message": "Employee not found"}), 404


@employees_bp.route("/<int:id>", methods=["DELETE"])
def delete_employee(id):
    employees = read_data()
    for emp in employees:
        if emp["EmployeeID"] == id:
            employees.remove(emp)
            write_data(employees)
            return jsonify({"message": "Employee deleted"})
    return jsonify({"message": "Employee not found"}), 404
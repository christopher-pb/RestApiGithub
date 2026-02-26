import json
from flask import request, jsonify
from . import employees_bp

DATA_FILE = "data/employees.json"


@employees_bp.route("/", methods=["GET"])
def get_employees():
    with open(DATA_FILE) as f:
        data = json.load(f)
    return jsonify(data["employees"])


@employees_bp.route("/", methods=["POST"])
def add_employee():
    new_employee = request.json

    with open(DATA_FILE) as f:
        data = json.load(f)

    data["employees"].append(new_employee)

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    return jsonify(new_employee), 201

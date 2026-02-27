from flask import Blueprint, jsonify, request
import json

department_bp = Blueprint("department", __name__)

FILE = "data/departments.json"


def read_data():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []


def write_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


@department_bp.route("/departments", methods=["GET"])
def get_departments():
    return jsonify(read_data())


@department_bp.route("/departments", methods=["POST"])
def add_department():
    departments = read_data()
    new_department = request.json
    departments.append(new_department)
    write_data(departments)
    return jsonify(new_department), 201
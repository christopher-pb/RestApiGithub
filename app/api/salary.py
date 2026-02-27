from flask import Blueprint, jsonify, request
import json

salary_bp = Blueprint("salary", __name__)

FILE = "data/salaries.json"


def read_data():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []


def write_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


@salary_bp.route("/salaries", methods=["GET"])
def get_salaries():
    return jsonify(read_data())


@salary_bp.route("/salaries", methods=["POST"])
def add_salary():
    salaries = read_data()
    new_salary = request.json
    salaries.append(new_salary)
    write_data(salaries)
    return jsonify(new_salary), 201
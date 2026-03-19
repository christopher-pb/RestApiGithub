from flask import Blueprint, jsonify
import json

bp = Blueprint('employees', __name__)

@bp.route('/employees', methods=['GET'])
def get_employees():
    with open('data/employees.json') as f:
        employees = json.load(f)
    return jsonify(employees)


@bp.route('/departments', methods=['GET'])
def get_departments():
    with open('data/departments.json') as f:
        departments = json.load(f)
    return jsonify(departments)


@bp.route('/salaries', methods=['GET'])
def get_salaries():
    with open('data/salaries.json') as f:
        salaries = json.load(f)
    return jsonify(salaries)
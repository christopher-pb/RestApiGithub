import json
from flask import Blueprint, request, jsonify

salaries_bp = Blueprint('salaries', __name__)

DATA_FILE = 'data/salaries.json'

def read_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@salaries_bp.route('/', methods=['GET'])
def get_salaries():
    return jsonify(read_data())

@salaries_bp.route('/<int:id>', methods=['GET'])
def get_salary(id):
    data = read_data()
    sal = next((s for s in data if s['SalaryID'] == id), None)
    if sal:
        return jsonify(sal)
    return {"message": "Not found"}, 404

@salaries_bp.route('/', methods=['POST'])
def add_salary():
    data = read_data()
    new = request.json
    data.append(new)
    write_data(data)
    return jsonify(new), 201

@salaries_bp.route('/<int:id>', methods=['PUT'])
def update_salary(id):
    data = read_data()
    for s in data:
        if s['SalaryID'] == id:
            s.update(request.json)
            write_data(data)
            return jsonify(s)
    return {"message": "Not found"}, 404

@salaries_bp.route('/<int:id>', methods=['DELETE'])
def delete_salary(id):
    data = read_data()
    data = [s for s in data if s['SalaryID'] != id]
    write_data(data)
    return {"message": "Deleted"}
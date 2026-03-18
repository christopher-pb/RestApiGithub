import json
from flask import Blueprint, request, jsonify

departments_bp = Blueprint('departments', __name__)

DATA_FILE = 'data/departments.json'

def read_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@departments_bp.route('/', methods=['GET'])
def get_departments():
    return jsonify(read_data())

@departments_bp.route('/<int:id>', methods=['GET'])
def get_department(id):
    data = read_data()
    dep = next((d for d in data if d['DepartmentID'] == id), None)
    if dep:
        return jsonify(dep)
    return {"message": "Not found"}, 404

@departments_bp.route('/', methods=['POST'])
def add_department():
    data = read_data()
    new = request.json
    data.append(new)
    write_data(data)
    return jsonify(new), 201

@departments_bp.route('/<int:id>', methods=['PUT'])
def update_department(id):
    data = read_data()
    for d in data:
        if d['DepartmentID'] == id:
            d.update(request.json)
            write_data(data)
            return jsonify(d)
    return {"message": "Not found"}, 404

@departments_bp.route('/<int:id>', methods=['DELETE'])
def delete_department(id):
    data = read_data()
    data = [d for d in data if d['DepartmentID'] != id]
    write_data(data)
    return {"message": "Deleted"}
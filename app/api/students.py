from flask import Blueprint, request, jsonify

bp = Blueprint("students", __name__)

students = []

@bp.route("/students", methods=["GET"])
def list_students():
    return jsonify(students), 200


@bp.route("/students", methods=["POST"])
def create_student():
    data = request.get_json()
    students.append(data)
    return jsonify(data), 201


@bp.route("/students/<int:id>", methods=["GET"])
def get_student(id):
    if id < len(students):
        return jsonify(students[id]), 200
    return jsonify({"error": "Student not found"}), 404


@bp.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.get_json()
    if id < len(students):
        students[id] = data
        return jsonify(data), 200
    return jsonify({"error": "Student not found"}), 404


@bp.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    if id < len(students):
        students.pop(id)
        return "", 204
    return jsonify({"error": "Student not found"}), 404

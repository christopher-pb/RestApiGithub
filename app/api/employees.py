from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

students_bp = Blueprint("students", __name__)

students = []
current_id = 1


@students_bp.route("", methods=["POST"])
@jwt_required()
def create_student():
    global current_id

    data = request.get_json() or {}

    if "name" not in data or "age" not in data:
        return jsonify({"message": "Invalid data"}), 400

    student = {
        "id": current_id,
        "name": data["name"],
        "age": data["age"]
    }

    students.append(student)
    current_id += 1

    return jsonify({"student": student}), 201


@students_bp.route("", methods=["GET"])
@jwt_required()
def list_students():
    return jsonify({"students": students}), 200


@students_bp.route("/<int:student_id>", methods=["GET"])
@jwt_required()
def get_student(student_id):
    for student in students:
        if student["id"] == student_id:
            return jsonify({"student": student}), 200
    return jsonify({"message": "Student not found"}), 404


@students_bp.route("/<int:student_id>", methods=["PUT"])
@jwt_required()
def update_student(student_id):
    data = request.get_json() or {}

    for student in students:
        if student["id"] == student_id:
            student["name"] = data.get("name", student["name"])
            student["age"] = data.get("age", student["age"])
            return jsonify({"student": student}), 200

    return jsonify({"message": "Student not found"}), 404


@students_bp.route("/<int:student_id>", methods=["DELETE"])
@jwt_required()
def delete_student(student_id):
    global students

    for student in students:
        if student["id"] == student_id:
            students = [s for s in students if s["id"] != student_id]
            return jsonify({"message": "Student deleted"}), 200

    return jsonify({"message": "Student not found"}), 404
from flask import Blueprint, request, jsonify

bp = Blueprint("auth", __name__)

users = []

@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Missing fields"}), 400

    for user in users:
        if user["username"] == data["username"]:
            return jsonify({"error": "User already exists"}), 409

    users.append(data)
    return jsonify({"message": "User registered"}), 201


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    for user in users:
        if user["username"] == data["username"]:
            if user["password"] == data["password"]:
                return jsonify({"message": "login successful"}), 200
            else:
                return jsonify({"message": "invalid credentials"}), 401

    return jsonify({"message": "user not found"}), 404

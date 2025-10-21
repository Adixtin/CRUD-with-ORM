from flask import Blueprint, request, jsonify
from app.service.user_service import UserService

user_service = UserService()
user_bp = Blueprint("user", __name__)

@user_bp.route("/users", methods=["GET"])
def get_all_users():
    users = user_service.get_all_users()
    return jsonify([user.to_dict() for user in users]), 200

@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    user = user_service.get_user_by_id(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"message": "User not found"}), 404

@user_bp.route("/users/username/<string:username>", methods=["GET"])
def get_user_by_username(username):
    user = user_service.get_user_by_username(username)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"message": "User not found"}), 404

@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    user = user_service.create_user(
        username=data["username"],
        role=data.get("role", "user")
    )
    return jsonify(user.to_dict()), 201

@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    success = user_service.delete_user(user_id)
    if success:
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"message": "User not found"}), 404

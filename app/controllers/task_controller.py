from flask import Blueprint, request, jsonify
from app.service.task_service import TaskService

task_service = TaskService()
task_bp = Blueprint("task", __name__)

@task_bp.route("/tasks", methods=["GET"])
def get_all_tasks():
    tasks = task_service.get_all_tasks()
    return jsonify([task.to_dict() for task in tasks]), 200

@task_bp.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = task_service.get_task_by_id(task_id)
    if task:
        return jsonify(task.to_dict()), 200
    return jsonify({"message": "Task not found"}), 404

@task_bp.route("/tasks/user/<int:user_id>", methods=["GET"])
def get_tasks_by_user(user_id):
    tasks = task_service.get_tasks_by_user(user_id)
    return jsonify([task.to_dict() for task in tasks]), 200

@task_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    task = task_service.create_task(
        user_id=data["user_id"],
        task_name=data["task_name"],
        due_date=data["due_date"],
        status=data.get("status", "pending"),
        priority=data.get("priority", "medium")
    )
    return jsonify(task.to_dict()), 201

@task_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    success = task_service.delete_task(task_id)
    if success:
        return jsonify({"message": "Task deleted"}), 200
    return jsonify({"message": "Task not found"}), 404

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.task import Task
from app import db

task_bp = Blueprint("tasks", __name__)


@task_bp.route("/", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()

    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 5))

    tasks = Task.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page)

    return {
        "tasks": [task.to_dict() for task in tasks.items],
        "total": tasks.total,
        "pages": tasks.pages
    }, 200


@task_bp.route("/", methods=["POST"])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.get_json()

    task = Task(
        title=data["title"],
        description=data.get("description"),
        user_id=user_id
    )

    db.session.add(task)
    db.session.commit()

    return task.to_dict(), 201


@task_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def update_task(id):
    user_id = get_jwt_identity()
    task = Task.query.get_or_404(id)

    if task.user_id != user_id:
        return {"error": "Unauthorized"}, 403

    data = request.get_json()

    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)

    db.session.commit()

    return task.to_dict(), 200


@task_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_task(id):
    user_id = get_jwt_identity()
    task = Task.query.get_or_404(id)

    if task.user_id != user_id:
        return {"error": "Unauthorized"}, 403

    db.session.delete(task)
    db.session.commit()

    return {"message": "Deleted"}, 200
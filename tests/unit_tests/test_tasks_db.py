import pytest
import datetime
from sqlalchemy.exc import IntegrityError
from app.models.task_model import Task
from app.models.database import db
from app.db.db_task import get_task_by_id, create_task, delete_task, get_tasks_by_user

@pytest.fixture
def app():
    from flask import Flask
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def session(app):
    return db.session

def test_create_task(session):
    from app.models.user_model import User
    from app.db.db_task import create_task, get_task_by_id

    # Create a user first
    user = User(username="Alice", role="admin")
    session.add(user)
    session.commit()

    due_date = datetime.datetime(2024, 9, 14, 12, 0, 0)

    # Use exact enum values (lowercase)
    task = create_task(user.user_id, "shopping", due_date, "pending", "high")

    assert task.task_id is not None
    assert task.user_id == user.user_id
    assert task.task_name == "shopping"
    assert task.status.value == "pending"
    assert task.priority.value == "high"
    assert task.due_date == due_date

    fetched = get_task_by_id(task.task_id)
    assert fetched is not None
    assert fetched.task_name == "shopping"

def test_get_task_by_id_returns_none(session):
    fetched = get_task_by_id(999)
    assert fetched is None

def test_get_tasks_by_user(session):
    due_date = datetime.datetime(2024, 9, 14, 12, 0, 0)
    t1 = create_task(1, "Task1", due_date, "pending", "medium")
    t2 = create_task(1, "Task2", due_date, "in_progress", "high")
    t3 = create_task(2, "Task3", due_date, "completed", "low")

    tasks_user1 = get_tasks_by_user(1)
    assert tasks_user1 is not None
    assert tasks_user1.task_id in [t1.task_id, t2.task_id]

def test_delete_task(session):
    due_date = datetime.datetime(2024, 9, 14, 12, 0, 0)
    task = create_task(1, "to_delete", due_date, "PENDING", "LOW")

    result = delete_task(task.task_id)
    assert result is True
    assert get_task_by_id(task.task_id) is None

    # Deleting non-existent task
    result = delete_task(9999)
    assert result is False

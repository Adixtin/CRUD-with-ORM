import pytest
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import db
from app.models.task_model import Task, Status, Priority
from app.repositories.db_task import TaskORM, get_tasks_by_user, get_task_by_id, create_task, delete_task

@pytest.fixture(scope="module")
def test_app():
    from flask import Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def session(test_app):
    with test_app.app_context():
        yield db.session
        db.session.rollback()


def test_create_task(session):
    task = Task(user_id=1, task_name="Test ORM Task", due_date=datetime.datetime(2025, 12, 31))
    created = create_task(task)

    assert created.task_id is not None
    assert created.task_name == "Test ORM Task"
    assert created.status == Status.PENDING
    assert created.priority == Priority.MEDIUM

    orm_task = TaskORM.query.get(created.task_id)
    assert orm_task.task_name == "Test ORM Task"


def test_get_task_by_id(session):
    task = Task(user_id=2, task_name="Find Me Task")
    created = create_task(task)

    found = get_task_by_id(created.task_id)
    assert found is not None
    assert found.task_name == "Find Me Task"

    not_found = get_task_by_id(9999)
    assert not_found is None


def test_get_tasks_by_user(session):
    tasks = [
        Task(user_id=3, task_name="Task 1"),
        Task(user_id=3, task_name="Task 2"),
        Task(user_id=4, task_name="Other User Task")
    ]
    for t in tasks:
        create_task(t)

    user_tasks = get_tasks_by_user(3)
    assert len(user_tasks) == 2
    assert all(t.user_id == 3 for t in user_tasks)


def test_delete_task(session):
    task = Task(user_id=5, task_name="Delete Me")
    created = create_task(task)

    success = delete_task(created.task_id)
    assert success is True

    assert get_task_by_id(created.task_id) is None

    fail = delete_task(9999)
    assert fail is False

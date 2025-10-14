import pytest
import datetime
from app.models.task_model import db, Task

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

def test_task_id_and_creation_time(session):
    task = Task(task_name="Task")
    session.add(task)
    session.commit()

    fetched = Task.query.first()

    assert fetched.task_id is not None
    assert isinstance(fetched.task_id, int)

    assert fetched.creation_time is not None
    assert isinstance(fetched.creation_time, datetime.datetime)

    assert fetched.status == Task.Status.PENDING
    assert fetched.priority == Task.Priority.MEDIUM

    assert fetched.task_name == "Task"

def test_task_with_fixed_times(session):
    fixed_creation = datetime.datetime(2024, 9, 14, 12, 0, 0)
    fixed_due = datetime.datetime(2024, 9, 20, 18, 30, 0)

    task = Task(
        task_name="fixed time task",
        creation_time=fixed_creation,
        due_date=fixed_due,
        status=Task.Status.IN_PROGRESS,
        priority=Task.Priority.HIGH
    )
    session.add(task)
    session.commit()

    fetched = Task.query.first()

    assert fetched.task_name == "fixed time task"
    assert fetched.creation_time == fixed_creation
    assert fetched.due_date == fixed_due
    assert fetched.status == Task.Status.IN_PROGRESS
    assert fetched.priority == Task.Priority.HIGH
    assert fetched.task_id is not None


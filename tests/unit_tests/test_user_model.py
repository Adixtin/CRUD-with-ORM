import pytest
import datetime
from app.models.user_model import db, User

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

def test_user_creation_time_and_id(session):
    user = User(username="User", role="user")
    session.add(user)
    session.commit()

    fetched = User.query.first()

    assert fetched.user_id is not None
    assert isinstance(fetched.user_id, int)

    assert fetched.created_at is not None
    assert isinstance(fetched.created_at, datetime.datetime)

    assert fetched.username == "User"
    assert fetched.role == "user"

def test_task_with_fixed_times(session):
    fixed_created_at = datetime.datetime(2024, 9, 14, 12, 0, 0)

    user = User(
        username="fixed time User",
        role="fixed time user",
        created_at=fixed_created_at,
    )
    session.add(user)
    session.commit()

    fetched = User.query.first()

    assert fetched.username == "fixed time User"
    assert fetched.role == "fixed time user"
    assert fetched.created_at == fixed_created_at
    assert fetched.user_id is not None


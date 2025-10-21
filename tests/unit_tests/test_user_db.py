import pytest
import datetime
from app.models.database import db
from app.models.user_model import User
from app.repositories.db_user import UserORM, get_all_users, get_user_by_id, create_user, delete_user

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


def test_create_user(session):
    user = User(user_id=1, username="alice", role="admin", created_at=datetime.datetime(2025, 10, 21))
    created = create_user(user)

    assert created.user_id == 1
    assert created.username == "alice"
    assert created.role == "admin"

    orm_user = UserORM.query.get(1)
    assert orm_user.username == "alice"


def test_get_user_by_id(session):
    user = User(user_id=2, username="bob", role="user", created_at=datetime.datetime.now())
    create_user(user)

    found = get_user_by_id(2)
    assert found.username == "bob"
    assert found.role == "user"


def test_get_all_users(session):
    users = [
        User(user_id=3, username="charlie", role="moderator", created_at=datetime.datetime.now()),
        User(user_id=4, username="dave", role="user", created_at=datetime.datetime.now()),
    ]
    for u in users:
        create_user(u)

    all_users = get_all_users()
    assert isinstance(all_users, list)
    assert len(all_users[0]) >= 2


def test_delete_user(session):
    user = User(user_id=5, username="eve", role="user", created_at=datetime.datetime.now())
    create_user(user)

    success = delete_user(5)
    assert success is True
    assert UserORM.query.get(5) is None

    fail = delete_user(999)
    assert fail is False

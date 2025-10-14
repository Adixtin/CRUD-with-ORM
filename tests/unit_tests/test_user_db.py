import pytest
from sqlalchemy.exc import IntegrityError
from app.models.user_model import User
from app.models.database import db
from app.db.db_user import get_all_users, get_user_by_id, create_user, delete_user

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

def test_create_user(session):
    user = create_user("Alice", "admin")

    assert user.user_id is not None
    assert user.username == "Alice"
    assert user.role == "admin"

    fetched = User.query.get(user.user_id)
    assert fetched is not None
    assert fetched.username == "Alice"

def test_get_all_users(session):
    create_user("Bob", "user")
    create_user("Charlie", "user")

    users = get_all_users()
    assert len(users) == 2
    usernames = [u.username for u in users]
    assert "Bob" in usernames
    assert "Charlie" in usernames

def test_get_user_by_id(session):
    user = create_user("Diana", "admin")

    fetched = get_user_by_id(user.user_id)
    assert fetched is not None
    assert fetched.username == "Diana"

    assert get_user_by_id(9999) is None

def test_delete_user(session):
    user = create_user("Eve", "user")

    result = delete_user(user.user_id)
    assert result is True
    assert get_user_by_id(user.user_id) is None

    result = delete_user(9999)
    assert result is False

def test_create_user_duplicate(session):
    create_user("Frank", "user")
    with pytest.raises(IntegrityError):
        create_user("Frank", "admin")

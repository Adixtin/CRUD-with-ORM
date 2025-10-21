import datetime
from app.models.user_model import User


def test_user_initialization():
    now = datetime.datetime(2025, 10, 21, 5, 0, 0)
    user = User(user_id=1, username="alice", role="admin", created_at=now)

    assert user.user_id == 1
    assert user.username == "alice"
    assert user.role == "admin"
    assert user.created_at == now
    assert isinstance(user.created_at, datetime.datetime)


def test_user_to_dict():
    now = datetime.datetime(2025, 10, 21)
    user = User(user_id=2, username="bob", role="user", created_at=now)

    result = user.to_dict()

    assert result == {
        "user_id": 2,
        "username": "bob",
        "role": "user",
    }


def test_user_repr():
    user = User(user_id=3, username="charlie", role="moderator", created_at=datetime.datetime.now())
    assert repr(user) == "<User charlie>"

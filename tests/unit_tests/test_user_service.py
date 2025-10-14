import pytest
from unittest.mock import patch, MagicMock
from app.service.user_service import UserService

service = UserService()


@pytest.fixture
def fake_user():
    user = MagicMock()
    user.user_id = 1
    user.username = "Alice"
    user.role = "admin"
    return user


def test_create_user(fake_user):
    with patch("app.service.user_service.db.session.add") as mock_add, \
         patch("app.service.user_service.db.session.commit") as mock_commit, \
         patch("app.service.user_service.User", return_value=fake_user):

        user = service.create_user(username="Alice", role="admin")

        mock_add.assert_called_once_with(fake_user)
        mock_commit.assert_called_once()
        assert user.user_id == fake_user.user_id
        assert user.username == "Alice"
        assert user.role == "admin"


def test_get_user_by_id(fake_user):
    fake_user_class = MagicMock()
    fake_user_class.query.get.return_value = fake_user

    with patch("app.service.user_service.User", fake_user_class):
        user = service.get_user_by_id(1)
        fake_user_class.query.get.assert_called_once_with(1)
        assert user.username == "Alice"


def test_get_user_by_id_none():
    fake_user_class = MagicMock()
    fake_user_class.query.get.return_value = None

    with patch("app.service.user_service.User", fake_user_class):
        user = service.get_user_by_id(999)
        fake_user_class.query.get.assert_called_once_with(999)
        assert user is None


def test_get_user_by_username(fake_user):
    fake_user_class = MagicMock()
    fake_user_class.query.filter_by.return_value.first.return_value = fake_user

    with patch("app.service.user_service.User", fake_user_class):
        user = service.get_user_by_username("Alice")
        fake_user_class.query.filter_by.assert_called_once_with(username="Alice")
        assert user.username == "Alice"


def test_get_user_by_username_none():
    fake_user_class = MagicMock()
    fake_user_class.query.filter_by.return_value.first.return_value = None

    with patch("app.service.user_service.User", fake_user_class):
        user = service.get_user_by_username("Bob")
        fake_user_class.query.filter_by.assert_called_once_with(username="Bob")
        assert user is None


def test_delete_user_success(fake_user):
    fake_user_class = MagicMock()
    fake_user_class.query.get.return_value = fake_user

    with patch("app.service.user_service.User", fake_user_class), \
         patch("app.service.user_service.db.session.delete") as mock_delete, \
         patch("app.service.user_service.db.session.commit") as mock_commit:

        result = service.delete_user(1)
        fake_user_class.query.get.assert_called_once_with(1)
        mock_delete.assert_called_once_with(fake_user)
        mock_commit.assert_called_once()
        assert result is True


def test_delete_user_failure():
    fake_user_class = MagicMock()
    fake_user_class.query.get.return_value = None

    with patch("app.service.user_service.User", fake_user_class):
        result = service.delete_user(999)
        fake_user_class.query.get.assert_called_once_with(999)
        assert result is False

import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch
from app.models.user_model import User
from app.service.user_service import UserService


@pytest.fixture
def sample_user():
    return User(user_id=1, username="alice", role="admin", created_at=None)


def test_get_all_users(sample_user):
    mock_orm_user = MagicMock(to_domain=MagicMock(return_value=sample_user))
    with patch("app.service.user_service.UserORM") as mock_orm:
        mock_orm.query.all.return_value = [mock_orm_user]

        result = UserService.get_all_users()
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].username == "alice"


def test_get_user_by_id_found(sample_user):
    mock_orm_user = MagicMock(to_domain=MagicMock(return_value=sample_user))
    with patch("app.service.user_service.UserORM") as mock_orm:
        mock_orm.query.get.return_value = mock_orm_user

        result = UserService.get_user_by_id(1)
        assert result.username == "alice"
        mock_orm.query.get.assert_called_once_with(1)


def test_get_user_by_id_not_found():
    with patch("app.service.user_service.UserORM") as mock_orm:
        mock_orm.query.get.return_value = None

        result = UserService.get_user_by_id(999)
        assert result is None


def test_get_user_by_username(sample_user):
    mock_orm_user = MagicMock(to_domain=MagicMock(return_value=sample_user))
    with patch("app.service.user_service.UserORM") as mock_orm:
        mock_orm.query.get.return_value = mock_orm_user

        result = UserService.get_user_by_username("alice")
        assert result.to_domain() == sample_user
        mock_orm.query.get.assert_called_once_with("alice")


def test_create_user():
    with patch("app.service.user_service.UserORM") as mock_orm, \
         patch("app.service.user_service.db.session") as mock_db_session:

        created_at = datetime.now()

        mock_orm_instance = MagicMock()
        mock_orm.from_domain.return_value = mock_orm_instance
        mock_orm_instance.to_domain.return_value = User(user_id=1, username="alice", role="user", created_at=created_at)

        result = UserService.create_user(username="alice", role="user")

        assert result.username == "alice"
        mock_orm.from_domain.assert_called_once()
        mock_db_session.add.assert_called_once_with(mock_orm_instance)
        mock_db_session.commit.assert_called_once()


def test_delete_user_success():
    mock_orm_instance = MagicMock()
    with patch("app.service.user_service.UserORM") as mock_orm, \
         patch("app.service.user_service.db.session") as mock_db_session:

        mock_orm.query.get.return_value = mock_orm_instance

        result = UserService.delete_user(1)
        assert result is True
        mock_db_session.delete.assert_called_once_with(mock_orm_instance)
        mock_db_session.commit.assert_called_once()


def test_delete_user_not_found():
    with patch("app.service.user_service.UserORM") as mock_orm:
        mock_orm.query.get.return_value = None

        result = UserService.delete_user(999)
        assert result is False

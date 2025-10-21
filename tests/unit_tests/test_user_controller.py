import pytest
from unittest.mock import MagicMock
from flask import Flask

from app.controllers.user_controller import user_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(user_bp)
    return app.test_client()


@pytest.fixture(autouse=True)
def mock_user_service(monkeypatch):
    mock_service = MagicMock()
    monkeypatch.setattr("app.controllers.user_controller.user_service", mock_service)
    return mock_service


def test_get_all_users(client, mock_user_service):
    mock_user_service.get_all_users.return_value = [
        MagicMock(to_dict=lambda: {"id": 1, "username": "alice"}),
        MagicMock(to_dict=lambda: {"id": 2, "username": "bob"}),
    ]

    response = client.get("/users")

    assert response.status_code == 200
    assert response.json == [
        {"id": 1, "username": "alice"},
        {"id": 2, "username": "bob"},
    ]
    mock_user_service.get_all_users.assert_called_once()


def test_get_user_by_id_found(client, mock_user_service):
    mock_user_service.get_user_by_id.return_value = MagicMock(
        to_dict=lambda: {"id": 1, "username": "alice"}
    )

    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json == {"id": 1, "username": "alice"}
    mock_user_service.get_user_by_id.assert_called_once_with(1)


def test_get_user_by_id_not_found(client, mock_user_service):
    mock_user_service.get_user_by_id.return_value = None

    response = client.get("/users/999")

    assert response.status_code == 404
    assert response.json == {"message": "User not found"}


def test_get_user_by_username_found(client, mock_user_service):
    mock_user_service.get_user_by_username.return_value = MagicMock(
        to_dict=lambda: {"id": 1, "username": "alice"}
    )

    response = client.get("/users/username/alice")

    assert response.status_code == 200
    assert response.json == {"id": 1, "username": "alice"}
    mock_user_service.get_user_by_username.assert_called_once_with("alice")


def test_get_user_by_username_not_found(client, mock_user_service):
    mock_user_service.get_user_by_username.return_value = None

    response = client.get("/users/username/unknown")

    assert response.status_code == 404
    assert response.json == {"message": "User not found"}


def test_create_user(client, mock_user_service):
    mock_user_service.create_user.return_value = MagicMock(
        to_dict=lambda: {"id": 1, "username": "charlie", "role": "user"}
    )

    payload = {"username": "charlie"}

    response = client.post("/users", json=payload)

    assert response.status_code == 201
    assert response.json == {"id": 1, "username": "charlie", "role": "user"}

    mock_user_service.create_user.assert_called_once_with(
        username="charlie", role="user"
    )


def test_delete_user_success(client, mock_user_service):
    mock_user_service.delete_user.return_value = True

    response = client.delete("/users/1")

    assert response.status_code == 200
    assert response.json == {"message": "User deleted"}
    mock_user_service.delete_user.assert_called_once_with(1)


def test_delete_user_not_found(client, mock_user_service):
    mock_user_service.delete_user.return_value = False

    response = client.delete("/users/999")

    assert response.status_code == 404
    assert response.json == {"message": "User not found"}

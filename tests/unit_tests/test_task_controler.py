import pytest
from unittest.mock import MagicMock
from flask import Flask
from app.controllers.task_controller import task_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(task_bp)
    client = app.test_client()
    return client


@pytest.fixture(autouse=True)
def mock_task_service(monkeypatch):
    mock_service = MagicMock()
    monkeypatch.setattr("app.controllers.task_controller.task_service", mock_service)
    return mock_service


def test_get_all_tasks(client, mock_task_service):
    mock_task_service.get_all_tasks.return_value = [
        MagicMock(to_dict=lambda: {"id": 1, "task_name": "Test Task"})
    ]

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json == [{"id": 1, "task_name": "Test Task"}]
    mock_task_service.get_all_tasks.assert_called_once()


def test_get_task_found(client, mock_task_service):
    mock_task_service.get_task_by_id.return_value = MagicMock(
        to_dict=lambda: {"id": 1, "task_name": "Found Task"}
    )

    response = client.get("/tasks/1")

    assert response.status_code == 200
    assert response.json == {"id": 1, "task_name": "Found Task"}
    mock_task_service.get_task_by_id.assert_called_once_with(1)


def test_get_task_not_found(client, mock_task_service):
    mock_task_service.get_task_by_id.return_value = None

    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json == {"message": "Task not found"}


def test_get_tasks_by_user(client, mock_task_service):
    mock_task_service.get_tasks_by_user.return_value = [
        MagicMock(to_dict=lambda: {"id": 1, "task_name": "User Task"})
    ]

    response = client.get("/tasks/user/10")

    assert response.status_code == 200
    assert response.json == [{"id": 1, "task_name": "User Task"}]
    mock_task_service.get_tasks_by_user.assert_called_once_with(10)


def test_create_task(client, mock_task_service):
    mock_task_service.create_task.return_value = MagicMock(
        to_dict=lambda: {"id": 1, "task_name": "Created Task"}
    )

    payload = {
        "user_id": 1,
        "task_name": "Created Task",
        "due_date": "2025-10-21",
        "status": "pending",
        "priority": "high",
    }

    response = client.post("/tasks", json=payload)

    assert response.status_code == 201
    assert response.json == {"id": 1, "task_name": "Created Task"}

    mock_task_service.create_task.assert_called_once_with(
        user_id=1,
        task_name="Created Task",
        due_date="2025-10-21",
        status="pending",
        priority="high"
    )


def test_delete_task_success(client, mock_task_service):
    mock_task_service.delete_task.return_value = True

    response = client.delete("/tasks/1")

    assert response.status_code == 200
    assert response.json == {"message": "Task deleted"}
    mock_task_service.delete_task.assert_called_once_with(1)


def test_delete_task_not_found(client, mock_task_service):
    mock_task_service.delete_task.return_value = False

    response = client.delete("/tasks/999")

    assert response.status_code == 404
    assert response.json == {"message": "Task not found"}

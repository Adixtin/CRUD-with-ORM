import datetime
import pytest
from unittest.mock import patch, MagicMock
from app.service.task_service import TaskService

service = TaskService()

@pytest.fixture
def fake_task():
    task = MagicMock()
    task.task_id = 1
    task.user_id = 1
    task.task_name = "Test Task"
    task.status.value = "pending"
    task.priority.value = "medium"
    task.due_date = datetime.datetime(2024, 10, 14, 12, 0, 0)
    return task

def test_create_task(fake_task):
    with patch("app.service.task_service.Task", return_value=fake_task) as mock_task, \
         patch("app.service.task_service.db.session.add") as mock_add, \
         patch("app.service.task_service.db.session.commit") as mock_commit:

        task = service.create_task(
            user_id=1,
            task_name="Test Task",
            due_date=fake_task.due_date,
            status="pending",
            priority="medium"
        )

        mock_task.assert_called_once()
        mock_add.assert_called_once_with(fake_task)
        mock_commit.assert_called_once()
        assert task.task_id == 1
        assert task.task_name == "Test Task"
        assert task.status.value == "pending"
        assert task.priority.value == "medium"

def test_get_task_by_id():
    fake_task = MagicMock()
    fake_task.task_name = "Test Task"

    fake_task_class = MagicMock()
    fake_task_class.query.get.return_value = fake_task

    with patch("app.service.task_service.Task", fake_task_class):
        task = service.get_task_by_id(1)
        fake_task_class.query.get.assert_called_once_with(1)
        assert task.task_name == "Test Task"

def test_get_task_by_id_none():
    fake_task_class = MagicMock()
    fake_task_class.query.get.return_value = None

    with patch("app.service.task_service.Task", fake_task_class):
        task = service.get_task_by_id(999)
        fake_task_class.query.get.assert_called_once_with(999)
        assert task is None

def test_get_tasks_by_user():
    fake_task = MagicMock()
    fake_task_class = MagicMock()
    fake_task_class.query.filter_by.return_value.all.return_value = [fake_task]

    with patch("app.service.task_service.Task", fake_task_class):
        tasks = service.get_tasks_by_user(1)
        fake_task_class.query.filter_by.assert_called_once_with(user_id=1)
        assert tasks == [fake_task]

def test_delete_task_success():
    fake_task = MagicMock()
    fake_task_class = MagicMock()
    fake_task_class.query.get.return_value = fake_task

    with patch("app.service.task_service.Task", fake_task_class), \
         patch("app.service.task_service.db.session.delete") as mock_delete, \
         patch("app.service.task_service.db.session.commit") as mock_commit:

        result = service.delete_task(1)
        fake_task_class.query.get.assert_called_once_with(1)
        mock_delete.assert_called_once_with(fake_task)
        mock_commit.assert_called_once()
        assert result is True
        
def test_delete_task_failure():
    fake_task_class = MagicMock()
    fake_task_class.query.get.return_value = None

    with patch("app.service.task_service.Task", fake_task_class):
        result = service.delete_task(999)
        fake_task_class.query.get.assert_called_once_with(999)
        assert result is False
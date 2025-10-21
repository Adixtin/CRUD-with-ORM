import datetime
import pytest
from unittest.mock import MagicMock, patch
from app.models.task_model import Task, Status, Priority
from app.service.task_service import TaskService


@pytest.fixture
def sample_task():
    return Task(
        user_id=1,
        task_name="Test Task",
        task_id=10,
        creation_time=datetime.datetime(2025, 10, 21),
        due_date=datetime.datetime(2025, 12, 31),
        status=Status.PENDING,
        priority=Priority.MEDIUM
    )


def test_get_all_tasks(sample_task):
    mock_orm_task = MagicMock(to_domain=MagicMock(return_value=sample_task))
    with patch("app.service.task_service.TaskORM") as mock_orm:
        mock_orm.query.all.return_value = [mock_orm_task]

        result = TaskService.get_all_tasks()
        assert len(result) == 1
        assert result[0].task_name == "Test Task"


def test_get_task_by_id_found(sample_task):
    mock_orm_task = MagicMock(to_domain=MagicMock(return_value=sample_task))
    with patch("app.service.task_service.TaskORM") as mock_orm:
        mock_orm.query.get.return_value = mock_orm_task

        result = TaskService.get_task_by_id(10)
        assert result.task_name == "Test Task"
        mock_orm.query.get.assert_called_once_with(10)


def test_get_task_by_id_not_found():
    with patch("app.service.task_service.TaskORM") as mock_orm:
        mock_orm.query.get.return_value = None

        result = TaskService.get_task_by_id(999)
        assert result is None


def test_get_tasks_by_user(sample_task):
    mock_orm_task = MagicMock(to_domain=MagicMock(return_value=sample_task))
    with patch("app.service.task_service.TaskORM") as mock_orm:
        mock_orm.query.filter_by.return_value.all.return_value = [mock_orm_task]

        result = TaskService.get_tasks_by_user(user_id=1)
        assert len(result) == 1
        assert result[0].user_id == 1
        mock_orm.query.filter_by.assert_called_once_with(user_id=1)


def test_create_task():
    with patch("app.service.task_service.TaskORM") as mock_orm, \
         patch("app.service.task_service.db.session") as mock_db_session:

        mock_orm_instance = MagicMock()
        mock_orm.from_domain.return_value = mock_orm_instance
        mock_orm_instance.to_domain.return_value = Task(
            user_id=1,
            task_name="Created Task",
            task_id=1,
            status=Status.PENDING,
            priority=Priority.MEDIUM
        )

        result = TaskService.create_task(
            user_id=1,
            task_name="Created Task",
            status="pending",
            priority="medium"
        )

        assert result.task_name == "Created Task"
        mock_orm.from_domain.assert_called_once()
        mock_db_session.add.assert_called_once_with(mock_orm_instance)
        mock_db_session.commit.assert_called_once()


def test_delete_task_success():
    mock_orm_instance = MagicMock()
    with patch("app.service.task_service.TaskORM") as mock_orm, \
         patch("app.service.task_service.db.session") as mock_db_session:

        mock_orm.query.get.return_value = mock_orm_instance

        result = TaskService.delete_task(1)
        assert result is True
        mock_db_session.delete.assert_called_once_with(mock_orm_instance)
        mock_db_session.commit.assert_called_once()


def test_delete_task_not_found():
    with patch("app.service.task_service.TaskORM") as mock_orm:
        mock_orm.query.get.return_value = None

        result = TaskService.delete_task(999)
        assert result is False

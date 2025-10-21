import datetime
import pytest
from app.models.task_model import Task, Status, Priority  # adjust import to your path


def test_task_defaults():
    """Test that Task initializes with correct default values."""
    task = Task(user_id=1, task_name="Test Task")

    assert task.user_id == 1
    assert task.task_name == "Test Task"
    assert task.status == Status.PENDING
    assert task.priority == Priority.MEDIUM
    assert isinstance(task.creation_time, datetime.datetime)
    assert task.due_date is None
    assert "<Task Test Task>" in repr(task)


def test_task_to_dict_with_due_date():
    """Test that to_dict includes all fields with a due date."""
    due_date = datetime.datetime(2025, 12, 25, 12, 0, 0)
    creation_time = datetime.datetime(2025, 10, 21, 8, 0, 0)

    task = Task(
        task_id=10,
        user_id=5,
        task_name="Finish Project",
        creation_time=creation_time,
        due_date=due_date,
        status=Status.IN_PROGRESS,
        priority=Priority.HIGH
    )

    result = task.to_dict()

    assert result["task_id"] == 10
    assert result["user_id"] == 5
    assert result["task_name"] == "Finish Project"
    assert result["status"] == "in_progress"
    assert result["priority"] == "high"
    assert result["creation_time"] == creation_time.isoformat()
    assert result["due_date"] == due_date.isoformat()


def test_task_to_dict_without_due_date():
    """Test to_dict when due_date is None."""
    creation_time = datetime.datetime(2025, 1, 1, 10, 0, 0)
    task = Task(
        task_id=3,
        user_id=2,
        task_name="Read Book",
        creation_time=creation_time,
        due_date=None,
    )

    result = task.to_dict()

    assert result["due_date"] is None
    assert result["creation_time"] == creation_time.isoformat()
    assert result["status"] == "pending"
    assert result["priority"] == "medium"


def test_enum_values():
    """Ensure enum string values are correct."""
    assert Status.PENDING.value == "pending"
    assert Status.IN_PROGRESS.value == "in_progress"
    assert Status.COMPLETED.value == "completed"

    assert Priority.LOW.value == "low"
    assert Priority.MEDIUM.value == "medium"
    assert Priority.HIGH.value == "high"


def test_task_repr():
    """Ensure the __repr__ returns a readable format."""
    task = Task(user_id=1, task_name="Homework")
    assert repr(task) == "<Task Homework>"

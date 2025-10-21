import datetime
from enum import Enum
from dataclasses import dataclass
from typing import Optional

class Status(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@dataclass
class Task:
    user_id: int
    task_name: str
    task_id: Optional[int] = None
    creation_time: datetime.datetime = datetime.datetime.now()
    due_date: Optional[datetime.datetime] = None
    status: Status = Status.PENDING
    priority: Priority = Priority.MEDIUM

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "user_id": self.user_id,
            "task_name": self.task_name,
            "creation_time": self.creation_time.isoformat(),
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "status": self.status.value,
            "priority": self.priority.value,
        }

    def __repr__(self):
        return f"<Task {self.task_name}>"

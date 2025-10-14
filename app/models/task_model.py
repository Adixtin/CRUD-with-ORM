import datetime
from enum import Enum
from .database import db

class Task (db.Model):
    __tablename__ = 'tasks'

    class Status(Enum):
        PENDING = "pending"
        IN_PROGRESS = "in_progress"
        COMPLETED = "completed"

    class Priority(Enum):
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"

    task_id: int = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    task_name: str = db.Column(db.String, nullable=False)
    creation_time: datetime.datetime = db.Column(db.DateTime, default=datetime.datetime.now)
    due_date: datetime.datetime = db.Column(db.DateTime)
    status: Status = db.Column(db.Enum(Status), default=Status.PENDING ,nullable=False)
    priority: Priority = db.Column(db.Enum(Priority), default=Priority.MEDIUM ,nullable=False)

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "user_id": self.user_id,
            "task_name": self.task_name,
            "creation_time": self.creation_time.isoformat() if self.creation_time else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "status": self.status.value if self.status else self.status.PENDING,
            "priority": self.priority.value if self.priority else self.priority.MEDIUM,
        }

    def __repr__(self) -> str:
        return f"<Task {self.task_name}>"

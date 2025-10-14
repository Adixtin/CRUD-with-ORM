import datetime
from email.policy import default
from enum import Enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    task_name: str = db.Column(db.String, nullable=False)
    creation_time: datetime.datetime = db.Column(db.DateTime, default=datetime.datetime.now)
    due_date: datetime.datetime = db.Column(db.DateTime)
    status: Status = db.Column(db.Enum(Status), default=Status.PENDING ,nullable=False)
    priority: Priority = db.Column(db.Enum(Priority), default=Priority.MEDIUM ,nullable=False)

    def __repr__(self) -> str:
        return f"<Task {self.task_name}"

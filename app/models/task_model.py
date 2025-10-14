import datetime
from enum import Enum
from .user_model import User
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

    def __repr__(self) -> str:
        return f"<Task {self.task_name}>"

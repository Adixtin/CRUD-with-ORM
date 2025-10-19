import datetime
from typing import List, Optional
from app.models.database import db
from app.models.task_model import Task, Status, Priority

class TaskORM(db.Model):
    __tablename__ = "tasks"

    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    task_name = db.Column(db.String, nullable=False)
    creation_time = db.Column(db.DateTime, default=db.func.now())
    due_date = db.Column(db.DateTime)
    status = db.Column(db.Enum(Status), default=Status.PENDING, nullable=False)
    priority = db.Column(db.Enum(Priority), default=Priority.MEDIUM, nullable=False)

    def to_domain(self) -> Task:
        task = Task(
            user_id=self.user_id,
            task_name=self.task_name,
            creation_time=self.creation_time,
            due_date=self.due_date,
            status=self.status,
            priority=self.priority
        )
        task.task_id = self.task_id
        return task

    @staticmethod
    def from_domain(task: Task) -> "TaskORM":
        return TaskORM(
            user_id=task.user_id,
            task_name=task.task_name,
            creation_time=task.creation_time,
            due_date=task.due_date,
            status=task.status,
            priority=task.priority
        )

# --- Repository functions ---

def get_tasks_by_user(user_id: int) -> List[Task]:
    orm_tasks = TaskORM.query.filter_by(user_id=user_id).all()
    return [t.to_domain() for t in orm_tasks]

def get_task_by_id(task_id: int) -> Optional[Task]:
    orm_task = TaskORM.query.get(task_id)
    return orm_task.to_domain() if orm_task else None

def create_task(task: Task) -> Task:
    orm_task = TaskORM.from_domain(task)
    db.session.add(orm_task)
    db.session.commit()
    return orm_task.to_domain()

def delete_task(task_id: int) -> bool:
    orm_task = TaskORM.query.get(task_id)
    if orm_task:
        db.session.delete(orm_task)
        db.session.commit()
        return True
    return False

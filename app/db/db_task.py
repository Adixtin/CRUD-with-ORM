import datetime
from typing import List

from app.models.task_model import Task
from app.models.database import db

def get_tasks_by_user(user_id: int) -> List[Task]:
    return Task.query.get(user_id)

def get_task_by_id(task_id: int) -> Task:
    return Task.query.get(task_id)

def create_task(user_id: int,task_name: str, due_date: datetime.datetime, status: str, priority: str) -> Task:
    task = Task(
        user_id=user_id,
        task_name=task_name,
        due_date=due_date,
        status=Task.Status[status.upper()],
        priority=Task.Priority[priority.upper()]
    )
    db.session.add(task)
    db.session.commit()
    return task

def delete_task(task_id: int) -> bool:
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return True
    return False

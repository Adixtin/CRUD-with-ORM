import datetime
from typing import List

from app.models.task_model import task_db, Task

def get_tasks_by_user(user_id: int) -> List[Task]:
    return Task.query.get(user_id)

def get_task_by_id(task_id: int) -> Task:
    return Task.query.get(task_id)

def create_task(user_id: int,task_name: str, due_date: datetime.datetime, status: Task.Status, priority: Task.Priority) -> Task:
    task = Task(user_id=user_id, task_name=task_name, due_date=due_date, status=status, priority=priority)
    task_db.session.add(task)
    task_db.session.commit()
    return task

def delete_task(task_id: int) -> bool:
    task = Task.query.get(task_id)
    if task:
        task_db.session.delete(task)
        task_db.session.commit()
        return True
    return False

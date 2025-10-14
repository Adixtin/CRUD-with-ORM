from typing import List, Optional
from datetime import datetime
from app.models.task_model import Task
from app.models.database import db


class TaskService:

    @staticmethod
    def get_all_tasks() -> List[Task]:
        return Task.query.all()

    @staticmethod
    def get_task_by_id(task_id: int) -> Optional[Task]:
        return Task.query.get(task_id)

    @staticmethod
    def get_tasks_by_user(user_id: int) -> List[Task]:
        return Task.query.filter_by(user_id=user_id).all()

    @staticmethod
    def create_task(
            user_id: int,
            task_name: str,
            due_date: datetime,
            status: str = "pending",
            priority: str = "medium"
    ) -> Task:
        status_enum = Task.Status[status.upper()]
        priority_enum = Task.Priority[priority.upper()]

        task = Task(
            user_id=user_id,
            task_name=task_name,
            due_date=due_date,
            status=status_enum,
            priority=priority_enum
        )
        db.session.add(task)
        db.session.commit()
        return task

    @staticmethod
    def delete_task(task_id: int) -> bool:
        task = Task.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
            return True
        return False

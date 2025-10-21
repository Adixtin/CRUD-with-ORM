from typing import List, Optional
from datetime import datetime
from app.models.task_model import Task, Status, Priority  # for domain model and enums
from app.repositories.db_task import TaskORM, get_task_by_id as repo_get_task_by_id
from app.models.database import db

class TaskService:

    @staticmethod
    def get_all_tasks() -> List[Task]:
        return [t.to_domain() for t in TaskORM.query.all()]

    @staticmethod
    def get_task_by_id(task_id: int) -> Optional[Task]:
        orm_task = TaskORM.query.get(task_id)
        if orm_task is None:
            return None
        return orm_task.to_domain()
    @staticmethod
    def get_tasks_by_user(user_id: int) -> List[Task]:
        return [t.to_domain() for t in TaskORM.query.filter_by(user_id=user_id).all()]

    @staticmethod
    def create_task(
            user_id: int,
            task_name: str,
            due_date: Optional[datetime] = None,
            status: str = "pending",
            priority: str = "medium"
    ) -> Task:
        status_enum = Status[status.upper()]
        priority_enum = Priority[priority.upper()]

        domain_task = Task(
            user_id=user_id,
            task_name=task_name,
            due_date=due_date,
            status=status_enum,
            priority=priority_enum
        )
        orm_task = TaskORM.from_domain(domain_task)
        db.session.add(orm_task)
        db.session.commit()
        return orm_task.to_domain()

    @staticmethod
    def delete_task(task_id: int) -> bool:
        orm_task = TaskORM.query.get(task_id)
        if orm_task:
            db.session.delete(orm_task)
            db.session.commit()
            return True
        return False

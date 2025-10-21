from typing import List, Optional
from datetime import datetime
from app.models.user_model import User
from app.repositories.db_user import UserORM
from app.repositories.db_task import TaskORM
from app.models.database import db


class UserService:

    @staticmethod
    def get_all_users() -> List[User]:
        return [t.to_domain() for t in UserORM.query.all()]

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        orm_user = UserORM.query.get(user_id)
        if orm_user is None:
            return None
        return orm_user.to_domain()

    @staticmethod
    def get_user_by_username(username: str) -> Optional[User]:
        return UserORM.query.get(username)

    @staticmethod
    def create_user(
            username: str,
            role: str = "user",
    ) -> User:

        domain_user = User(
            username=username,
            role=role,
            created_at=datetime.now(),
        )
        orm_user = UserORM.form_domain(domain_user)
        db.session.add(orm_user)
        db.session.commit()
        return orm_user.to_domain()

    @staticmethod
    def delete_user(user_id: int) -> bool:
        tasks = TaskORM.query.filter_by(user_id=user_id).all()
        for t in tasks:
            db.session.delete(t)
        db.session.commit()

        orm_user = UserORM.query.get(user_id)
        if orm_user:
            db.session.delete(orm_user)
            db.session.commit()
            return True
        return False
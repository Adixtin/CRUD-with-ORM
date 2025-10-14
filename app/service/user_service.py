from typing import List, Optional
from app.models.user_model import User
from app.models.database import db


class UserService:

    @staticmethod
    def get_all_users() -> List[User]:
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_username(username: str) -> Optional[User]:
        return User.query.filter_by(username=username).first()

    @staticmethod
    def create_user(username: str, role: str = "user") -> User:
        user = User(username=username, role=role)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id: int) -> bool:
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False

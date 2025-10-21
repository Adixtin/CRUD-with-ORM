from typing import List

from app.models.user_model import User
from app.models.database import db
from sqlalchemy.orm import relationship

class UserORM(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    
    tasks = relationship("TaskORM", backref="user", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "role": self.role,
            "created_at": self.created_at.isoformat(),
            "tasks": [task.to_dict() for task in self.tasks]
        }

    def to_domain(self) -> User:
        user = User(
            user_id=self.user_id,
            username=self.username,
            role=self.role,
            created_at=self.created_at,
        )
        return user

    @staticmethod
    def form_domain(user: User) -> "UserORM":
        return UserORM(
            user_id=user.user_id,
            username=user.username,
            role=user.role,
            created_at=user.created_at,
        )

def get_all_users() -> List[User]:
    return [UserORM.query.all()]

def get_user_by_id(user_id: int) -> User:
    orm_user = UserORM.query.get(user_id)
    return orm_user.to_domain()

def create_user(user: User) -> User:
    orm_user = UserORM.form_domain(user)
    db.session.add(orm_user)
    db.session.commit()
    return orm_user.to_domain()

def delete_user(user_id: int) -> bool:
    orm_user = UserORM.query.get(user_id)
    if orm_user:
        db.session.delete(orm_user)
        db.session.commit()
        return True
    return False

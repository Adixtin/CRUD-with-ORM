from typing import List

from app.models.user_model import db, User

def get_all_users() -> List[User]:
    return User.query.all()

def get_user_by_id(user_id: int) -> User:
    return User.query.get(user_id)

def create_user(username: str, role: str) -> User:
    user = User(username=username, role=role)
    db.session.add(user)
    db.session.commit()
    return user

def delete_user(user_id: int) -> bool:
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False

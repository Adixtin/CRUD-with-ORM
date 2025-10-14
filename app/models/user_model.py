from datetime import datetime
from .database import db


class User (db.Model):
    __tablename__ = 'users'

    user_id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(64), unique=True, nullable=False)
    role: str = db.Column(db.String(64), nullable=False)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "role": self.role
        }

    def __repr__(self) -> str:
        return f"<User {self.username}>"

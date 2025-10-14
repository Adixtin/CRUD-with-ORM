from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User (db.Model):
    __tablename__ = 'users'

    user_id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(64), unique=True, nullable=False)
    role: str = db.Column(db.String(64), nullable=False)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self) -> str:
        return f"<User {self.username}>"

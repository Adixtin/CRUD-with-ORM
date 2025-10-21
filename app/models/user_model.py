from datetime import datetime
from dataclasses import dataclass

@dataclass
class User:
    user_id: int
    username: str
    role: str
    created_at: datetime

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "role": self.role
        }

    def __repr__(self) -> str:
        return f"<User {self.username}>"

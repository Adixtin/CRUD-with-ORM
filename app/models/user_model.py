from datetime import datetime
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    user_id: Optional[int] = None
    username: str = ""
    role: str = "user"
    created_at: Optional[datetime] = None

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "role": self.role
        }

    def __repr__(self) -> str:
        return f"<User {self.username}>"

from datetime import datetime

from pydantic import BaseModel

from user.models import User


class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime

    @classmethod
    def build(cls, user: User):
        return cls(
            id=user.id,
            username=user.username,
            created_at=user.created_at
        )

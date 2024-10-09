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


class FriendResponse(BaseModel):
    id: int
    username: str


class FriendListResponse(BaseModel):
    friends: list[FriendResponse]

    @classmethod
    def build(cls, friends: list[tuple[int, str]]):
        return cls(friends=[FriendResponse(id=f[0], username=f[1]) for f in friends])

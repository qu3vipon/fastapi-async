from datetime import datetime

from pydantic import BaseModel

from user.models import User


class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime

    @classmethod
    def build(cls, user: User):
        return cls(id=user.id, username=user.username, created_at=user.created_at)


class UserListResponse(BaseModel):
    users: list[UserResponse]

    @classmethod
    def build(cls, users: list[User]):
        return cls(users=[UserResponse.build(user=u) for u in users])


class UserTokenResponse(BaseModel):
    access_token: str
    @classmethod
    def build(cls, access_token: str):
        return cls(access_token=access_token)

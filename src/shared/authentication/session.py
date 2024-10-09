from typing import ClassVar

from fastapi import Request

from user.models import User


class InvalidSessionKeyError(Exception):
    message: str = "Invalid Session Key"


class SessionService:
    SESSION_KEY: ClassVar[str] = "UserID"

    @staticmethod
    def login(request: Request, user: User):
        request.session[SessionService.SESSION_KEY] = user.id

    @staticmethod
    def authenticate(request: Request) -> int:
        if user_id := request.session.get(SessionService.SESSION_KEY):
            return user_id
        raise InvalidSessionKeyError

from typing import ClassVar

from fastapi import Request, HTTPException
from fastapi import status

from shared.config import settings
from user.models import User


class SessionMiddlewareRequiredError(Exception):
    message: str = "SessionMiddleware Required"


class SessionService:
    SESSION_KEY: ClassVar[str] = "UserId"

    @staticmethod
    def validate_session(request: Request):
        if not hasattr(request, "session"):
            raise SessionMiddlewareRequiredError

    def login(self, request: Request, user: User):
        self.validate_session(request=request)
        request.session[SessionService.SESSION_KEY] = user.id

    @classmethod
    def session_authenticate(cls, request: Request) -> int:
        cls.validate_session(request=request)

        if user_id := request.session.get(SessionService.SESSION_KEY):
            return user_id
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Session Key")

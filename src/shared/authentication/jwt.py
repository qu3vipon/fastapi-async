import time
from typing import ClassVar, TypedDict

import jwt

from shared.config import settings


class JWTPayloadTypedDict(TypedDict):
    user_id: int
    isa: float  # issued at (UNIX timestamp)


class InvalidTokenError(Exception):
    message = "Invalid Token"


class JWTService:
    SECRET_KEY: ClassVar[str] = settings.app_secret_key
    ALGORITHM: ClassVar[str] = "HS256"
    EXPIRY_SECONDS: ClassVar[int] = 24 * 60 * 60

    def encode_access_token(self, user_id: int) -> str:
        payload: JWTPayloadTypedDict = {"user_id": user_id, "isa": time.time()}
        return jwt.encode(payload=payload, key=self.SECRET_KEY, algorithm=self.ALGORITHM)

    def decode_access_token(self, access_token: str) -> JWTPayloadTypedDict:
        try:
            payload: JWTPayloadTypedDict = jwt.decode(
                jwt=access_token, key=self.SECRET_KEY, algorithms=[self.ALGORITHM]
            )
        except jwt.DecodeError:
            raise InvalidTokenError
        try:
            payload["user_id"] and payload["isa"]
        except KeyError:
            raise InvalidTokenError
        return payload

    def is_valid_token(self, payload: JWTPayloadTypedDict) -> bool:
        return time.time() < payload["isa"] + self.EXPIRY_SECONDS

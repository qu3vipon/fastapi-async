from datetime import datetime

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import TIMESTAMP

from shared.database.orm import Base


__all__ = [
    "User",
]


class User(Base):
    __tablename__ = "service_user"

    id = Column(Integer, primary_key=True)
    username = Column(String(16), nullable=False)
    password_hash = Column(String(60), nullable=False)
    created_at = Column(TIMESTAMP(precision=6), default=datetime.utcnow, nullable=False)

    @classmethod
    def create(cls, username: str, password_hash: str):
        return cls(username=username, password_hash=password_hash)

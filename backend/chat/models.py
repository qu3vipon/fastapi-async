from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, CheckConstraint, String, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import TIMESTAMP

from shared.database.orm import Base
from user.models import User


__all__ = [
    "ChatRoom",
    "ChatMessage",
]


class ChatRoom(Base):
    __tablename__ = "chat_room"
    id = Column(Integer, primary_key=True)
    user_one_id = Column(Integer, ForeignKey("service_user.id", ondelete="CASCADE"), nullable=False)
    user_two_id = Column(Integer, ForeignKey("service_user.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(precision=6), default=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("user_one_id", "user_two_id", name="uidx_chat_room_users"),
        CheckConstraint('user_one_id < user_two_id', name='user_one_less_than_user_two'),
    )

    @classmethod
    def create(cls, me_id: int, friend_id: int):
        assert me_id != friend_id

        if me_id < friend_id:
            return cls(user_one_id=me_id, user_two_id=friend_id)
        else:
            return cls(user_one_id=friend_id, user_two_id=me_id)


class ChatMessage(Base):
    __tablename__ = "chat_message"

    id = Column(Integer, primary_key=True)
    chat_room_id = Column(Integer, ForeignKey("chat_room.id", ondelete="CASCADE"), nullable=False)
    sender_id = Column(Integer, ForeignKey("service_user.id", ondelete="CASCADE"), nullable=False)
    contents = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP(precision=6), default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("idx_chat_messages", "chat_room_id", "created_at"),
    )

    @classmethod
    def create(cls, chat_room_id: int, sender_id: int, contents: str):
        return cls(chat_room_id=chat_room_id, sender_id=sender_id, contents=contents)

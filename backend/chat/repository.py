from fastapi import Depends
from sqlalchemy import or_, select, case
from sqlalchemy.orm import Session, aliased

from chat.models import ChatRoom
from shared.database.connection import get_db
from shared.database.repository import RDBRepository
from user.models import User


class ChatRepository(RDBRepository):
    def get_chat_rooms(self, user_id: int):
        UserOne = aliased(User)
        UserTwo = aliased(User)

        return self.db.execute(
            select(
                ChatRoom.id,
                case(
                    (ChatRoom.user_one_id == user_id, UserTwo.id),
                    else_=UserOne.id
                ).label('friend_id'),
                case(
                    (ChatRoom.user_one_id == user_id, UserTwo.username),
                    else_=UserOne.username
                ).label('friend_name'),
            )
            .select_from(ChatRoom)
            .join(
                UserOne, ChatRoom.user_one_id == UserOne.id,
            )
            .join(
                UserTwo, ChatRoom.user_two_id == UserTwo.id,
            )
            .where(
                or_(
                    ChatRoom.user_one_id == user_id,
                    ChatRoom.user_two_id == user_id,
                )
            )
        )

    def get_chat_room(self, me_id: int, chat_room_id: int) -> ChatRoom | None:
        return self.db.query(ChatRoom).filter(
            ChatRoom.id == chat_room_id,
            or_(
                ChatRoom.user_one_id == me_id,
                ChatRoom.user_two_id == me_id,
            )
        ).first()

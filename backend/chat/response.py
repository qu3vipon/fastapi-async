from pydantic import BaseModel


class _ChatRoomResponse(BaseModel):
    id: int
    friend_id: int
    friend_username: str

    @classmethod
    def build(cls, id: int, friend_id: int, friend_username: str):
        return cls(id=id, friend_id=friend_id, friend_username=friend_username)


class ChatRoomListResponse(BaseModel):
    chat_rooms: list[_ChatRoomResponse]

    @classmethod
    def build(cls, chat_rooms: list[tuple[int, int, str]]):
        return cls(
            chat_rooms=[
                _ChatRoomResponse.build(id=room_id, friend_id=friend_id, friend_username=friend_username)
                for room_id, friend_id, friend_username in chat_rooms
            ]
        )

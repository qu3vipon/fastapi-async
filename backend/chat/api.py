from fastapi import APIRouter, status, Depends, Body, HTTPException
from sqlalchemy.exc import IntegrityError

from chat.models import ChatRoom, ChatMessage
from chat.repository import ChatRepository
from chat.response import ChatRoomListResponse
from shared.authentication.dependency import authenticate

router = APIRouter(prefix="/chat-rooms", tags=["Chats"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ChatRoomListResponse,
)
def get_chat_rooms_handler(
    me_id: int = Depends(authenticate),
    chat_repo: ChatRepository = Depends(),
):
    chat_rooms: list[tuple[int, int, str]] = chat_repo.get_chat_rooms(user_id=me_id)
    return ChatRoomListResponse.build(chat_rooms=chat_rooms)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
def create_chat_room_handler(
    me_id: int = Depends(authenticate),
    friend_id: int = Body(..., embed=True),
    chat_repo: ChatRepository = Depends(),
):
    chat_room = ChatRoom.create(me_id=me_id, friend_id=friend_id)

    try:
        chat_repo.save(instance=chat_room)
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="ChatRoom Already Exists")
    return {"detail": "success"}

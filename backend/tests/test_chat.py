from schema import Schema
from sqlalchemy import exists

from chat.models import ChatRoom


class TestChat:
    def test_get_chat_rooms(self, client, test_session, test_user, access_token, test_friend):
        # given
        chat_room = ChatRoom.create(me_id=test_user.id, friend_id=test_friend.id)
        test_session.add(chat_room)
        test_session.commit()

        # when
        response = client.get("/chat-rooms", headers={"Authorization": f"Bearer {access_token}"})

        # then
        assert response.status_code == 200

        assert Schema(
            {
                "id": chat_room.id,
                "friend_id": test_friend.id,
                "friend_username": test_friend.username,
            }
        ).validate(response.json()["chat_rooms"][0])

    def test_create_chat_room(self, client, test_session, test_user, access_token, test_friend):
        # given

        # when
        response = client.post(
            "/chat-rooms", headers={"Authorization": f"Bearer {access_token}"},
            json={"friend_id": test_friend.id}
        )

        # then
        assert response.status_code == 201

        assert test_session.query(
            exists().where(ChatRoom.user_one_id == test_user.id, ChatRoom.user_two_id == test_friend.id)
        ).scalar()

        # when: duplicate request
        response = client.post(
            "/chat-rooms", headers={"Authorization": f"Bearer {access_token}"},
            json={"friend_id": test_friend.id}
        )

        # then
        assert response.status_code == 409

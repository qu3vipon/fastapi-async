
from schema import Schema

from shared.authentication.jwt import JWTService
from shared.authentication.password import PasswordService
from user.models import User


class TestUser:
    def test_user_sign_up(self, client, test_session):
        # given

        # when
        response = client.post("/users/sign-up", json={"username": "test", "password": "test-pw"})

        # then
        assert response.status_code == 201
        assert Schema(
            {
                "id": int,
                "username": "test",
                "created_at": str,
            }
        ).validate(response.json())

        user = test_session.query(User).filter(User.username == "test").first()

        assert user
        assert PasswordService().check_password(plain_text="test-pw", hashed_password=user.password_hash)

    def test_log_in(self, client, test_session, test_user):
        # given
        # when
        response = client.post(
            "/users/login",
            json={"username": "test", "password": "test-pw"}
        )
        # then
        assert response.status_code == 200
        assert Schema({"access_token": str}).validate(response.json())

        token = response.json()["access_token"]
        payload = JWTService().decode_access_token(access_token=token)

        assert payload["user_id"] == test_user.id
        assert payload["isa"]

    def test_get_users(self, client, test_session, test_user, access_token, test_friend):
        # given

        # when
        response = client.get("/users", headers={"Authorization": f"Bearer {access_token}"})

        # then
        assert response.status_code == 200

        assert Schema(
            {
                "id": test_friend.id,
                "username": test_friend.username,
                "created_at": str,
            }
        ).validate(response.json()["users"][0])

import pytest
from schema import Schema
from sqlalchemy import select

from shared.authentication.jwt import JWTService
from shared.authentication.password import PasswordService
from user.models import User


@pytest.mark.asyncio
class TestUserAsync:
    async def test_user_sign_up(self, client, test_session, test_user):
        # given

        # when
        response = await client.post("/async/users/sign-up", json={"username": "test", "password": "test-pw"})

        # then
        assert response.status_code == 201
        assert Schema(
            {
                "id": int,
                "username": "test",
                "created_at": str,
            }
        ).validate(response.json())

        result = await test_session.execute(
            select(User).filter(User.username == "test")
        )
        user = result.scalars().first()

        assert user
        assert PasswordService().check_password(plain_text="test-pw", hashed_password=user.password_hash)

    async def test_log_in(self, client, test_session, test_user):
        # given

        # when
        response = await client.post("/async/users/login", json={"username": "test", "password": "test-pw"})

        # then
        assert response.status_code == 200
        assert Schema({"access_token": str}).validate(response.json())

        token = response.json()["access_token"]
        payload = JWTService().decode_access_token(access_token=token)

        assert payload["user_id"] == test_user.id
        assert payload["isa"]

    async def test_get_me(self, client, test_session, test_user, access_token):
        # given

        # when
        response = await client.get("/async/users/me", headers={"Authorization": f"Bearer {access_token}"})

        # then
        assert response.status_code == 200
        assert Schema(
            {
                "id": test_user.id,
                "username": test_user.username,
                "created_at": test_user.created_at.isoformat(),
            }
        ).validate(response.json())

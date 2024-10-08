from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from shared.authentication.password import PasswordService
from user.models import User
from user.repository import UserRepository
from user.request import UserAuthRequest
from user.response import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/sign-up",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
def sign_up_user_handler(
    body: UserAuthRequest,
    user_repo: UserRepository = Depends(),
    password_service: PasswordService = Depends(),
):
    if not user_repo.validate_username(username=body.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    new_user = User.create(
        username=body.username,
        password_hash=password_service.hash_password(plain_text=body.password),
    )
    user_repo.save(user=new_user)
    return UserResponse.build(user=new_user)

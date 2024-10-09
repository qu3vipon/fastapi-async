from fastapi import APIRouter, Depends, HTTPException, Request
from starlette import status

from shared.authentication.dependency import get_user_id
from shared.authentication.jwt import JWTService
from shared.authentication.password import PasswordService
from user.models import User
from user.repository import UserRepository
from user.request import UserAuthRequest
from user.response import FriendListResponse, UserResponse, UserTokenResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/sign-up",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
def user_sign_up_handler(
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


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=UserTokenResponse,
)
def user_login_handler(
    body: UserAuthRequest,
    user_repo: UserRepository = Depends(),
    jwt_service: JWTService = Depends(),
    password_service: PasswordService = Depends(),
):
    user: User | None = user_repo.get_user_by_username(username=body.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not password_service.check_password(plain_text=body.password, hashed_password=user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    access_token = jwt_service.encode_access_token(user_id=user.id)
    return UserTokenResponse.build(access_token=access_token)



@router.get(
    "/me/friends",
    status_code=status.HTTP_200_OK,
    response_model=FriendListResponse,
)
def get_user_friends_handler(
    user_id: int = Depends(get_user_id),
    user_repo: UserRepository = Depends(),
):
    user: User | None = user_repo.get_user_by_id(user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    friends: list[tuple[int, str]] = user_repo.get_friends(user_id=user_id)
    return FriendListResponse.build(friends=friends)

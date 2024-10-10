from fastapi import Depends
from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from shared.database.connection import get_db
from shared.database.repository import RDBRepository
from user.models import User


class UserRepository(RDBRepository):

    def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_users(self, me_id: int) -> list[User]:
        return list(self.db.query(User).filter(User.id != me_id).all())

    def validate_username(self, username: str) -> bool:
        return not self.db.query(exists().where(User.username == username)).scalar()

from fastapi import Depends
from sqlalchemy import exists
from sqlalchemy.orm import Session

from shared.database.connection import get_db
from user.models import User


class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def save(self, user: User):
        self.db.add(user)
        self.db.commit()

    def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def validate_username(self, username: str) -> bool:
        return not self.db.query(exists().where(User.username == username)).scalar()

    def validate_email(self, email: str) -> bool:
        return not self.db.query(exists().where(User.email == email)).scalar()

    def delete_user(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()

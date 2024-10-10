from sqlalchemy import exists

from shared.database.repository import RDBRepository
from user.models import User


class UserRepository(RDBRepository):

    def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def validate_username(self, username: str) -> bool:
        return not self.db.query(exists().where(User.username == username)).scalar()

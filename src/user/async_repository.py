from fastapi import Depends
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database.connection_async import get_async_db
from user.models import User


class UserRepository:
    def __init__(self, db: AsyncSession = Depends(get_async_db)):
        self.db = db

    async def save(self, user: User):
        self.db.add(user)
        await self.db.commit()

    async def get_user_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def get_user_by_username(self, username: str) -> User | None:
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalars().first()

    async def validate_username(self, username: str) -> bool:
        result = await self.db.execute(select(exists().where(User.username == username)))
        return result.scalars().first()

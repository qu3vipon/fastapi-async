import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession

from main import app
from shared.authentication.jwt import JWTService
from shared.authentication.password import PasswordService
from shared.database.connection_async import get_async_db
from shared.database.orm import Base
from user.models import User


@pytest_asyncio.fixture(scope="session")
async def test_async_db():
    test_db_url = "postgresql+asyncpg://chat:chat-pw@127.0.0.1:54320/test"
    engine = create_async_engine(test_db_url, poolclass=NullPool)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def test_session(test_async_db: AsyncEngine):
    async with test_async_db.connect() as connection:
        async with connection.begin() as transaction:
            async_session = AsyncSession(
                bind=connection,
                expire_on_commit=False,
                autocommit=False,
                autoflush=False,
                join_transaction_mode="create_savepoint",
            )

            yield async_session
            await transaction.rollback()


@pytest_asyncio.fixture
async def client(test_session):
    async def test_get_db():
        yield test_session

    app.dependency_overrides[get_async_db] = test_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture(scope="function")
async def test_user(test_session):
    password_hash = PasswordService().hash_password(plain_text="test-pw")
    user = User.create(username="test", password_hash=password_hash)
    test_session.add(user)
    await test_session.commit()
    return user


@pytest.fixture(scope="function")
def access_token(test_user):
    return JWTService().encode_access_token(user_id=test_user.id)

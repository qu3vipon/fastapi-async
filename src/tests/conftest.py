import base64
import json

import itsdangerous
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from main import app

from shared.authentication.password import PasswordService
from shared.config import settings
from shared.database.connection import get_db
from shared.database.orm import Base
from user.models import User, UserRelation


@pytest.fixture(scope="session")
def test_db():
    test_db_url = "postgresql://fast-async:fast-async-pw@127.0.0.1:54320/test"
    if not database_exists(test_db_url):
        create_database(test_db_url)

    engine = create_engine(test_db_url)
    Base.metadata.create_all(engine)
    try:
        yield engine
    finally:
        Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def test_session(test_db):
    connection = test_db.connect()

    connection.begin()
    session = sessionmaker()(bind=connection)

    yield session

    session.rollback()
    connection.close()


@pytest.fixture
def client(test_session):
    def test_get_db():
        yield test_session

    app.dependency_overrides[get_db] = test_get_db
    return TestClient(app=app)


@pytest.fixture(scope="function")
def test_user(test_session):
    password_hash = PasswordService().hash_password(plain_text="test-pw")
    user = User.create(username="test", password_hash=password_hash)
    test_session.add(user)
    test_session.commit()
    return user


@pytest.fixture(scope="function")
def test_login_session(test_user) -> str:
    raw_session: bytes = json.dumps({"UserID": test_user.id}).encode("utf-8")
    encoded_session: bytes = base64.b64encode(raw_session)
    signer = itsdangerous.TimestampSigner(settings.app_secret_key)
    return signer.sign(value=encoded_session).decode("utf-8")


@pytest.fixture(scope="function")
def test_user_relation(test_session, test_user):
    password_hash = PasswordService().hash_password(plain_text="friend-pw")
    friend = User.create(username="friend", password_hash=password_hash)
    test_session.add(friend)
    test_session.flush()

    relation = UserRelation.add_friend(me=test_user, friend=friend)
    test_session.add(relation)
    test_session.commit()
    return relation

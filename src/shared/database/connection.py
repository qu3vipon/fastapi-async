from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from shared.config import settings


# Sync
def get_engine():
    db_engine = create_engine(settings.db_url, pool_pre_ping=True)
    return db_engine


engine = get_engine()
SessionFactory = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()

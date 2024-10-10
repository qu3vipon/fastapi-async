from typing import TypeVar

from fastapi import Depends
from sqlalchemy.orm import Session

from shared.database.connection import get_db
from shared.database.orm import Base

Instance = TypeVar("Instance", bound=Base)


class RDBRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def save(self, instance: Instance):
        self.db.add(instance)
        self.db.commit()

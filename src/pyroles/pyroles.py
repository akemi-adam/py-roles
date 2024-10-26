from uuid import uuid4

from sqlalchemy.orm import declarative_base

from sqlalchemy import Integer, UUID, String
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()
UuidBase = declarative_base()


class Model(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class UuidModel(UuidBase):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
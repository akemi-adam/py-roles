from pyroles import Base, UuidBase, Model, UuidModel

from sqlalchemy import ForeignKey, Insert, Integer, String, UUID, insert
from sqlalchemy.orm import Session, Mapped, mapped_column, relationship, declared_attr

from typing import Type


class DefaultRole():
    __tablename__ = 'roles'
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    @declared_attr
    def users(cls):
        return relationship("User", secondary="user_role", back_populates="roles")


class Role(Model, DefaultRole):
    pass


class UuidRole(UuidModel, DefaultRole):
    pass

    

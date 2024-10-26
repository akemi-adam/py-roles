
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from unittest import TestCase, main

from sqlalchemy import create_engine, String
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, relationship

from pyroles import Base, Model
from pyroles.models import Role, RoleHelper, UserRole

from faker import Faker


class User(Model):
    __tablename__ = 'users'
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    roles = relationship("Role", secondary="user_role", back_populates="users")


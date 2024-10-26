from pyroles import Model, UuidModel

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class DefaultAction():
    __tablename__ = 'actions'
    name: Mapped[str] = mapped_column(String(100), nullable=False)


class Action(Model, DefaultAction):
    pass


class UuidAction(UuidModel, DefaultAction):
    pass


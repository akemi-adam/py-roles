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

    
class UserRole(Base):
    __tablename__ = "user_role"
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"), primary_key=True)


class UuidUserRole(UuidBase):
    __tablename__ = "user_role"
    user_id: Mapped[UUID] = mapped_column(String(36), ForeignKey("users.id"), primary_key=True)
    role_id: Mapped[UUID] = mapped_column(String(36), ForeignKey("roles.id"), primary_key=True)


class RoleHelper:
    def __init__(self, session: Session, role_model: Type[DefaultRole]):
        self.session = session
        self.user_role = UserRole if role_model == Role else UuidUserRole
        self.role_model = role_model
    
    def find_by_name(self, name: str) -> DefaultRole|None:
        return self.session.query(self.role_model).filter(self.role_model.name == name).first()
    
    def create_role(self, name: str) -> DefaultRole:
        role = self.role_model(name=name)
        self.session.add(role)
        try:
            self.session.commit()
            self.session.refresh(role)
        except Exception as e:
            self.session.rollback()
            print(str(e))
        return role
        
    def assign_role(self, name: str, user_id: int) -> None:
        try:
            role = self.find_by_name(name)
            stmt: Insert = insert(self.user_role).values(user_id=user_id, role_id=role.id)
            self.session.execute(stmt)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(str(e))

    def remove_role(self, name: str, user_id: int) -> None:
        role = self.find_by_name(name)
        user_role = self.session.query(self.user_role).filter_by(user_id=user_id, role_id=role.id).first()
        try:
            self.session.delete(user_role)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(str(e))
        
        
    def edit_role(self, name: str, newName: str) -> DefaultRole:
        role = self.find_by_name(name)
        role.name = newName
        try:
            self.session.commit()
            self.session.refresh(role)
        except Exception as e:
            self.session.rollback()
            print(str(e))
        return role
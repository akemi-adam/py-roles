
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from unittest import TestCase, main

from sqlalchemy import create_engine, String
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, relationship

from pyroles import UuidBase, UuidModel
from pyroles.models import UuidRole, RoleHelper, UuidUserRole

from faker import Faker


class User(UuidModel):
    __tablename__ = 'users'
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    roles = relationship("UuidRole", secondary="user_role", back_populates="users")

class TestRoles(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = create_engine('sqlite:///:memory:')
        cls.Session = sessionmaker(bind=cls.engine)
        UuidBase.metadata.create_all(cls.engine)
        cls.faker: Faker = Faker()
    
    def setUp(self):
        self.session = self.Session()
        user: User = User(name=self.faker.name())
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        self.user = user
        self.roleHelper = RoleHelper(self.session, UuidRole)
        
    def tearDown(self):
        self.session.close()
        self.roleHelper.session.close()
        
    def test_creation_of_a_role(self):
        roleName: str = self.faker.word()
        role: UuidRole = self.roleHelper.create_role(roleName)
        self.assertIsNotNone(role)
        self.assertEqual(role.name, roleName)
    
    def test_uuid(self):
        roleName: str = self.faker.word()
        role: UuidRole = self.roleHelper.create_role(roleName)
        self.assertIsInstance(role.id, str)
        
    def test_assign_a_role_for_a_user(self):
        roleName: str = self.faker.word()
        
        role: UuidRole = self.roleHelper.create_role(roleName)
        self.roleHelper.assign_role(roleName, self.user.id)
        
        userRole = self.session.query(UuidUserRole).filter_by(
            user_id=self.user.id,
            role_id=role.id
        ).first()
        
        self.assertIsNotNone(userRole)
        self.assertIsInstance(userRole, UuidUserRole)
        self.assertEqual(userRole.user_id, self.user.id)
        self.assertEqual(userRole.role_id, role.id)
        
    def test_removing_a_role_from_a_user(self):
        roleName: str = self.faker.word()
        
        role: UuidRole = self.roleHelper.create_role(roleName)
        self.roleHelper.assign_role(roleName, self.user.id)
        
        userRole = self.session.query(UuidUserRole).filter_by(
            user_id=self.user.id,
            role_id=role.id
        ).first()
        
        self.assertIsNotNone(userRole)
        self.assertIsInstance(userRole, UuidUserRole)
        self.assertEqual(userRole.user_id, self.user.id)
        self.assertEqual(userRole.role_id, role.id)
        
        self.roleHelper.remove_role(roleName, self.user.id)
        
        userRole = self.session.query(UuidUserRole).filter_by(
            user_id=self.user.id,
            role_id=role.id
        ).first()
        
        self.assertIsNone(userRole)
        
    def test_editing_a_role(self):
        roleName: str = self.faker.word()
        role: UuidRole = self.roleHelper.create_role(roleName)
        self.assertIsNotNone(role)
        self.assertEqual(role.name, roleName)
        newName: str = self.faker.word()
        role = self.roleHelper.edit_role(roleName, newName)
        self.assertIsNotNone(role)
        self.assertNotEqual(role.name, roleName)
        self.assertEqual(role.name, newName)
        
        
if __name__ == '__main__':
    main()
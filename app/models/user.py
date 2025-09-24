from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum
from app.db.base import Base
import enum

class UserRole(enum.Enum):
    employee = "employee"
    employer = "employer"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLAlchemyEnum(UserRole), nullable=False)
from pydantic import BaseModel, EmailStr
from app.models.user import UserRole

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: UserRole

class User(UserBase):
    id: int
    role: UserRole

    class Config:
        from_attributes = True
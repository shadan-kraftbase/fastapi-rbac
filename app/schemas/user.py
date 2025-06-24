from pydantic import BaseModel, EmailStr
from uuid import UUID
from enum import Enum

class Role(str, Enum):
    admin = "admin"
    user = "user"
    manager = "manager"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Role = Role.user

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    role: Role
    is_active: bool

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    role: Role | None = None
    is_active: bool | None = None
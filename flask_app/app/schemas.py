from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    active_sessions: int
    registration_date: int

class UserCreate(BaseModel):
    username: str = Field(..., min_length=1)
    email: EmailStr

class UserUpdate(BaseModel):
    id: int
    username: Optional[str] = Field(None, min_length=1)
    email: Optional[EmailStr] = None
    active_sessions: int

class UserDelete(BaseModel):
    id: int

class UserGet(BaseModel):
    id: int

class UserListAll(BaseModel):
    page: int

class UserListAllResponse(BaseModel):
    users: list
    total_pages: int
    current_page: int
    total_users: int


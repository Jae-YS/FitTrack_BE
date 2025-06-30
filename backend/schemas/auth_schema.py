from pydantic import BaseModel, EmailStr
from typing import Optional
from backend.schemas.user_schema import UserResponse


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    user: Optional[UserResponse]
    is_new: bool

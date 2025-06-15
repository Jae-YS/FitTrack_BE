from pydantic import BaseModel, EmailStr
from typing import Optional
from .user_schema import UserOut


class LoginRequest(BaseModel):
    email: EmailStr


class LoginResponse(BaseModel):
    user: Optional[UserOut]
    is_new: bool

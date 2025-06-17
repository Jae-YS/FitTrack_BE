from pydantic import BaseModel, EmailStr
from typing import Optional
from backend.models.schemas.user_schema import UserOut


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    user: Optional[UserOut]
    is_new: bool

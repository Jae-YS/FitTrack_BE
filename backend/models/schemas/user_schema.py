from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    height: float
    weight: float
    sex: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str]
    height: Optional[float]
    weight: Optional[float]
    sex: Optional[str]

    class Config:
        from_attributes = True

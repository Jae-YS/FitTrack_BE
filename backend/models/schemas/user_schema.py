from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    height: float
    weight: float
    sex: str
    password: str

    race_date: Optional[date]
    race_level: Optional[str]
    pr_5k: Optional[float]
    pr_10k: Optional[float]
    pr_half: Optional[float]
    pr_full: Optional[float]


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str]
    height: Optional[float]
    weight: Optional[float]
    sex: Optional[str]

    class Config:
        from_attributes = True

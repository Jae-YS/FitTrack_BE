from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional
from .personal_best_schema import PersonalBestCreate
from .race_plan_schema import RacePlanCreate


class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str]
    height_cm: Optional[float]
    sex: str


class UserRequest(UserBase):
    password: Optional[str] = None


class UserCreate(UserBase):
    personal_bests: Optional[List[PersonalBestCreate]] = []
    race_plans: Optional[List[RacePlanCreate]] = []
    password: str


class UserResponse(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

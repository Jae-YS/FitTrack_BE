from pydantic import BaseModel
from typing import Optional


class WorkoutBase(BaseModel):
    type: str
    description: Optional[str]
    duration_minutes: Optional[int]


class WorkoutCreate(WorkoutBase):
    user_id: int


class WorkoutOut(WorkoutBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

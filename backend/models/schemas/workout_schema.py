from pydantic import BaseModel
from typing import Optional


class WorkoutBase(BaseModel):
    type: str
    description: Optional[str]
    duration_minutes: Optional[int]

    distance_km: Optional[float]
    pace_min_per_km: Optional[float]
    effort_level: Optional[str]


class WorkoutCreate(WorkoutBase):
    user_id: int


class WorkoutOut(WorkoutBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

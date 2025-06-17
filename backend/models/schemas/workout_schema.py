from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class WorkoutBase(BaseModel):
    type: str
    description: Optional[str]
    duration_minutes: Optional[int]
    distance_km: Optional[float]
    pace_min_per_km: Optional[float]
    effort_level: Optional[str]


class WorkoutCreate(WorkoutBase):
    user_id: int
    log_date: Optional[date] = None  # allow passing in a specific date


class WorkoutOut(WorkoutBase):
    id: int
    user_id: int
    log_date: date
    calories_burned: Optional[float]

    class Config:
        from_attributes = True

from pydantic import BaseModel, ConfigDict
from typing import Optional
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
    log_date: Optional[date] = None


class WorkoutOut(WorkoutBase):
    id: int
    user_id: int
    log_date: date
    calories_burned: Optional[float]

    model_config = ConfigDict(from_attributes=True)

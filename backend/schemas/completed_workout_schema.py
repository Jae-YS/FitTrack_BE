from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date


class CompletedWorkoutBase(BaseModel):
    date: date
    workout_type: str
    description: Optional[str]
    duration_minutes: Optional[int]
    distance_km: Optional[float]
    pace_min_per_km: Optional[float]
    effort_level: Optional[str]


class CompletedWorkoutCreate(CompletedWorkoutBase):
    user_id: int
    planned_workout_id: Optional[int]


class CompletedWorkoutResponse(CompletedWorkoutBase):
    id: int
    user_id: int
    planned_workout_id: Optional[int]

    model_config = ConfigDict(from_attributes=True)

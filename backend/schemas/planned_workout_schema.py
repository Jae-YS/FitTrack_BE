from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date


class PlannedWorkoutBase(BaseModel):
    recommended_date: Optional[date]
    workout_type: str
    description: Optional[str]
    duration_minutes: Optional[int]
    distance_km: Optional[float]
    pace: Optional[str]


class PlannedWorkoutCreate(PlannedWorkoutBase):
    training_plan_id: int


class PlannedWorkoutResponse(PlannedWorkoutBase):
    id: int
    training_plan_id: int

    model_config = ConfigDict(from_attributes=True)

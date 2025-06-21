from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date


class SuggestedWorkoutOut(BaseModel):
    id: int
    week: int
    user_id: int
    recommended_date: date
    workout_type: str
    description: str
    duration_minutes: Optional[int]
    distance_km: Optional[float]
    distance_per_workout: Optional[float]
    pace: Optional[str]
    goal: Optional[str]
    focus: Optional[str]
    intensity: Optional[str]

    model_config = ConfigDict(from_attributes=True)

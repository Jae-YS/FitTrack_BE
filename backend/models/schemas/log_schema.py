from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date
from backend.models.schemas.workout_schema import WorkoutCreate, WorkoutOut


class DailyLogCreate(BaseModel):
    user_id: int
    date: date
    mood: Optional[str]
    sleep_hours: Optional[float]
    workouts: Optional[List[WorkoutCreate]] = []


class DailyLogOut(BaseModel):
    user_id: int
    date: date
    mood: Optional[str]
    sleep_hours: Optional[float]
    workouts: List[WorkoutOut] = []

    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from .workout_schema import WorkoutCreate, WorkoutOut


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

    class Config:
        from_attributes = True

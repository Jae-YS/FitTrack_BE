from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date
from backend.schemas.completed_workout_schema import (
    CompletedWorkoutCreate,
    CompletedWorkoutResponse,
)


class DailyLogCreate(BaseModel):
    user_id: int
    date: date
    mood: Optional[str]
    sleep_hours: Optional[float]
    workouts: Optional[List[CompletedWorkoutCreate]] = []


class DailyLogOut(BaseModel):
    user_id: int
    date: date
    mood: Optional[str]
    sleep_hours: Optional[float]
    workouts: List[CompletedWorkoutResponse] = []

    model_config = ConfigDict(from_attributes=True)


class DailyEntryBase(BaseModel):
    mood: Optional[str]
    sleep_hours: Optional[float]


class DailyEntryCreate(DailyEntryBase):
    date: date


class DailyEntryResponse(DailyEntryBase):
    user_id: int
    date: date

    class Config:
        orm_mode = True

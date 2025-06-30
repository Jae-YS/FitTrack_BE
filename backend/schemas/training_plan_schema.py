from typing import Optional
from pydantic import BaseModel, ConfigDict


class TrainingPlanBase(BaseModel):
    week: int
    goal: Optional[str]
    focus: Optional[str]
    intensity: Optional[str]


class TrainingPlanCreate(TrainingPlanBase):
    user_id: int


class TrainingPlanRequest(TrainingPlanBase):
    user_id: int


class TrainingPlanResponse(TrainingPlanBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)

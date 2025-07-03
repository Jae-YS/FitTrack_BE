from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional


class RacePlanBase(BaseModel):
    race_type: str
    race_date: date
    notes: Optional[str]


class RacePlanCreate(RacePlanBase):
    pass


class RacePlanResponse(RacePlanBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)

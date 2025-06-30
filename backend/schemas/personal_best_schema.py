from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional


class PersonalBestBase(BaseModel):
    distance_type: str
    time_minutes: float
    recorded_date: Optional[date]


class PersonalBestCreate(PersonalBestBase):
    pass


class PersonalBestResponse(PersonalBestBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel
from datetime import datetime


class SummaryOut(BaseModel):
    id: int
    workout_id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class SuggestionOut(BaseModel):
    id: int
    user_id: int
    content: str
    week_start: datetime
    created_at: datetime

    class Config:
        from_attributes = True

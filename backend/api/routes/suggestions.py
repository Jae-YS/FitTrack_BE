from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.models.schemas import SuggestedWorkoutOut

from backend.models.sql_models import SuggestedWorkout
from backend.db.session import get_db


router = APIRouter()


# Retrieves all suggested workouts for a given user, ordered by recommended date
@router.get("/suggested-workouts/{user_id}", response_model=list[SuggestedWorkoutOut])
def get_suggested_workouts(user_id: int, db: Session = Depends(get_db)):

    workouts = (
        db.query(SuggestedWorkout)
        .filter(SuggestedWorkout.user_id == user_id)
        .order_by(SuggestedWorkout.recommended_date.asc())
        .all()
    )

    return workouts

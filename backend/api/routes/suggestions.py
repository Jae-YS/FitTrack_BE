from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.models.schemas import SuggestedWorkoutOut

from backend.services.workout_service import get_workouts, get_next_workout
from backend.db.session import get_db


router = APIRouter()


# Retrieves all suggested workouts for a given user, ordered by recommended date
@router.get("/suggested-workouts/{user_id}", response_model=list[SuggestedWorkoutOut])
def get_suggested_workouts(user_id: int, db: Session = Depends(get_db)):
    workouts = get_workouts(user_id, db)
    if not workouts:
        return []

    return workouts


@router.get(
    "/next-suggested-workout/{user_id}", response_model=list[SuggestedWorkoutOut]
)
async def get_next_suggested_workout(user_id: int, db: Session = Depends(get_db)):
    workouts = await get_next_workout(user_id, db)
    if not workouts:
        return []
    return workouts

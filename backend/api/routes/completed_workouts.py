from backend.db.session import get_db
from backend.schemas.completed_workout_schema import CompletedWorkoutCreate
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.services.completed_workout_service import create_completed_workout

router = APIRouter(prefix="/workouts", tags=["Completed Workouts"])


# Add a completed workout
@router.post("/new-completed-workout", response_model=dict)
async def completed_workout(
    completed_workout: CompletedWorkoutCreate,
    db: Session = Depends(get_db),
):
    new_workout = create_completed_workout(db, completed_workout)
    return {
        "status": "workout logged",
        "log_date": new_workout.log_date,
        "workout_id": new_workout.id,
    }

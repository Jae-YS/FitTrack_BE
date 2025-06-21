import traceback
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
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


@router.post("/next-suggested-workout/{user_id}")
async def get_next_suggested_workout(user_id: int, db: Session = Depends(get_db)):
    try:
        print(f"Fetching next workout for user_id: {user_id}")
        workout = await get_next_workout(user_id, db)
        if not workout:
            return JSONResponse(
                status_code=200, content={"message": "Not Sunday", "generated": False}
            )
        return workout
    except Exception:
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Workout generation failed")

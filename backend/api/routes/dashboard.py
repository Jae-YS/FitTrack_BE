from fastapi import APIRouter, Depends
from requests import Session
from backend.db.session import get_db
from backend.services.dashboard_service import (
    build_weekly_dashboard_data,
    build_workout_history,
    get_weekly_progress_data,
)


router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# Get the workout history for a user
@router.get("/users/{user_id}/history")
def get_workout_history(user_id: int, db: Session = Depends(get_db)):
    return build_workout_history(user_id, db)


# Get the weekly dashboard data for a user
@router.get("/dashboard/weekly/{user_id}")
def get_weekly_dashboard_data(user_id: int, db: Session = Depends(get_db)):
    return build_weekly_dashboard_data(user_id, db)


# Provide this week's progress: sleep hours, suggested & actual distance
@router.get("/weekly-progress/{user_id}")
def get_weekly_progress(user_id: int, db: Session = Depends(get_db)):
    return get_weekly_progress_data(user_id, db)

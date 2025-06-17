from datetime import date
from http.client import HTTPException
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from backend.models.schemas.workout_schema import WorkoutCreate
from backend.models.schemas.log_schema import (
    DailyLogCreate,
)
from backend.models.sql_models import DailyLog
from backend.services.logging_service import log_entry, add_workout_to_log
from backend.tasks.summary import trigger_summary_generation
from backend.db.session import get_db

from backend.services.dashboard_service import (
    build_user_history,
    build_weekly_dashboard_data,
)

router = APIRouter()


@router.get("/log/exists/{user_id}")
def check_daily_log_exists(user_id: int, db: Session = Depends(get_db)):
    today = date.today()
    exists = (
        db.query(DailyLog).filter_by(user_id=user_id, date=today).first() is not None
    )
    return {"exists": exists}


@router.post("/log")
async def log_day(
    entry: DailyLogCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    log = log_entry(db, entry)
    background_tasks.add_task(trigger_summary_generation, entry.user_id, db)
    return {"status": "logged", "user_id": log.user_id, "date": log.date}


@router.post("/workouts")
async def log_workout(
    workout: WorkoutCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    new_workout = add_workout_to_log(db, workout.user_id, workout)
    return {
        "status": "workout logged",
        "log_date": new_workout.log_date,
        "workout_id": new_workout.id,
    }


@router.get("/dashboard/weekly/{user_id}")
def get_weekly_dashboard_data(user_id: int, db: Session = Depends(get_db)):
    return build_weekly_dashboard_data(user_id, db)


@router.get("/users/{user_id}/history")
def get_workout_history(user_id: int, db: Session = Depends(get_db)):
    return build_user_history(user_id, db)

from datetime import date, timedelta
from backend.models.sql_models import DailyLog
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session


from backend.models.schemas.workout_schema import WorkoutCreate
from backend.models.schemas.log_schema import DailyLogCreate

from backend.services.logging_service import log_entry, add_workout_to_log
from backend.tasks.summary import trigger_summary_generation
from backend.db.session import get_db
from backend.services.dashboard_service import (
    build_user_history,
    build_weekly_dashboard_data,
    get_weekly_progress_data,
)

router = APIRouter()


# Check if today's daily log already exists for the user
@router.get("/log/exists/{user_id}")
def check_daily_log_exists(user_id: int, db: Session = Depends(get_db)):
    today = date.today()
    exists = (
        db.query(DailyLog).filter_by(user_id=user_id, date=today).first() is not None
    )
    return {"exists": exists}


# Log a daily entry and trigger LLM background summary generation
@router.post("/log")
async def log_day(
    entry: DailyLogCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    log = log_entry(db, entry)
    background_tasks.add_task(trigger_summary_generation, entry.user_id, db)
    return {"status": "logged", "user_id": log.user_id, "date": log.date}


# Log a workout and associate it with the correct daily log
@router.post("/workouts")
async def log_workout(
    workout: WorkoutCreate,
    db: Session = Depends(get_db),
):
    new_workout = add_workout_to_log(db, workout.user_id, workout)
    return {
        "status": "workout logged",
        "log_date": new_workout.log_date,
        "workout_id": new_workout.id,
    }


# Get full weekly dashboard info (modularized in service)
@router.get("/dashboard/weekly/{user_id}")
def get_weekly_dashboard_data(user_id: int, db: Session = Depends(get_db)):
    return build_weekly_dashboard_data(user_id, db)


# Return complete workout history for a user
@router.get("/users/{user_id}/history")
def get_workout_history(user_id: int, db: Session = Depends(get_db)):
    return build_user_history(user_id, db)


# Helper to compute the start of the week (Sunday)
def get_previous_sunday(today: date) -> date:
    return today - timedelta(days=today.weekday() + 1 if today.weekday() != 6 else 0)


# Provide this week's progress: sleep hours, suggested & actual distance
@router.get("/weekly-progress/{user_id}")
def get_weekly_progress(user_id: int, db: Session = Depends(get_db)):
    return get_weekly_progress_data(user_id, db)

from datetime import date
from sqlalchemy.orm import Session
from models.sql_models import DailyLog, Workout
from models.schemas import DailyLogCreate
from models.schemas import WorkoutCreate


def log_entry(db: Session, entry_data: DailyLogCreate) -> DailyLog:
    # Create the daily log
    daily_log = DailyLog(
        user_id=entry_data.user_id,
        date=entry_data.date,
        mood=entry_data.mood,
        sleep_hours=entry_data.sleep_hours,
    )
    db.add(daily_log)
    db.commit()
    db.refresh(daily_log)

    # Create associated workouts
    for workout in entry_data.workouts:
        new_workout = Workout(
            user_id=entry_data.user_id,
            log_date=entry_data.date,
            type=workout.type,
            description=workout.description,
            duration_minutes=workout.duration_minutes,
        )
        db.add(new_workout)

    db.commit()
    return daily_log


def add_workout(db: Session, workout_data) -> Workout:
    log = get_or_create_daily_log(db, workout_data.user_id, date.today())
    workout = Workout(
        user_id=workout_data.user_id,
        log_date=log.date,
        type=workout_data.type,
        description=workout_data.description,
        duration_minutes=workout_data.duration_minutes,
    )
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout


def log_entry(db: Session, entry_data: DailyLogCreate) -> DailyLog:
    daily_log = DailyLog(
        user_id=entry_data.user_id,
        date=entry_data.date,
        mood=entry_data.mood,
        sleep_hours=entry_data.sleep_hours,
    )
    db.add(daily_log)
    db.commit()
    db.refresh(daily_log)
    return daily_log


def get_or_create_daily_log(db: Session, user_id: int, log_date: date) -> DailyLog:
    log = db.query(DailyLog).filter_by(user_id=user_id, date=log_date).first()
    if log:
        return log
    new_log = DailyLog(user_id=user_id, date=log_date)
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log


def add_workout_to_log(
    db: Session, user_id: int, workout_data: WorkoutCreate
) -> Workout:
    today = date.today()
    get_or_create_daily_log(db, user_id, today)
    workout = Workout(
        user_id=user_id,
        log_date=today,
        type=workout_data.type,
        description=workout_data.description,
        duration_minutes=workout_data.duration_minutes,
        distance_km=workout_data.distance_km,
        pace_min_per_km=workout_data.pace_min_per_km,
        effort_level=workout_data.effort_level,
    )
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout

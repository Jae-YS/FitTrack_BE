from collections import defaultdict
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.models.sql_models import DailyLog, SuggestedWorkout, Workout, DailyLog


def get_logs_and_workouts_between(
    user_id: int, start_date: date, end_date: date, db: Session
):
    logs = (
        db.query(DailyLog)
        .filter(
            DailyLog.user_id == user_id, DailyLog.date.between(start_date, end_date)
        )
        .all()
    )
    workouts = (
        db.query(Workout)
        .filter(
            Workout.user_id == user_id, Workout.log_date.between(start_date, end_date)
        )
        .all()
    )
    return logs, workouts


def build_weekly_dashboard_data(user_id: int, db: Session):
    today = date.today()
    last_sunday = today - timedelta(
        days=today.weekday() + 1 if today.weekday() < 6 else 0
    )
    week_end = last_sunday + timedelta(days=6)

    logs, workouts = get_logs_and_workouts_between(user_id, last_sunday, week_end, db)

    workouts_by_date = defaultdict(list)
    for w in workouts:
        workouts_by_date[w.log_date].append(w)

    day_data = []
    for i in range(7):
        current_date = last_sunday + timedelta(days=i)
        w_today = workouts_by_date.get(current_date, [])
        total_cals = sum(w.calories_burned or 0 for w in w_today)

        day_data.append(
            {
                "day": current_date.strftime("%A"),
                "date": current_date.strftime("%m/%d"),
                "completed": bool(w_today),
                "expectedCalories": round(total_cals),
                "workouts": [
                    {
                        "type": w.type,
                        "durationMinutes": w.duration_minutes,
                        "calories_burned": w.calories_burned,
                    }
                    for w in w_today
                ],
            }
        )

    workout_data = [
        {
            "date": w.log_date.isoformat(),
            "type": w.type,
            "duration": w.duration_minutes,
            "calories": w.calories_burned,
            "description": w.description,
            "summary": "Generated summary here",
        }
        for w in workouts
    ]

    return {"days": day_data, "entries": workout_data}


def build_user_history(user_id: int, db: Session):
    today = date.today()
    start_date = today - timedelta(days=41)  # inclusive
    logs, workouts = get_logs_and_workouts_between(user_id, start_date, today, db)

    workouts_by_date = defaultdict(list)
    for w in workouts:
        workouts_by_date[w.log_date].append(w)

    summary_data = []
    for log in logs:
        total_minutes = sum(
            w.duration_minutes for w in workouts_by_date.get(log.date, [])
        )
        summary_data.append(
            {
                "date": log.date.isoformat(),
                "sleep_hours": log.sleep_hours,
                "total_workout_minutes": total_minutes,
            }
        )

    workout_entries = [
        {
            "date": w.log_date.isoformat(),
            "type": w.type,
            "duration": w.duration_minutes,
            "calories": w.calories_burned or 0,
            "description": w.description,
            "summary": "Generated summary placeholder",
        }
        for w in workouts
    ]

    return {"summary": summary_data, "entries": workout_entries}


def get_previous_sunday(today: date) -> date:
    return today - timedelta(days=today.weekday() + 1 if today.weekday() != 6 else 0)


def get_weekly_progress_data(user_id: int, db: Session) -> dict:
    today = datetime.now().date()
    start_of_week = get_previous_sunday(today)

    # Get one representative suggested workout's distance (they're all the same)
    suggested_workout = (
        db.query(SuggestedWorkout.distance_km)
        .filter(SuggestedWorkout.user_id == user_id)
        .filter(SuggestedWorkout.recommended_date >= start_of_week)
        .filter(SuggestedWorkout.recommended_date <= today)
        .first()
    )
    distance_km_suggested = suggested_workout[0] if suggested_workout else 0.0

    # Sum sleep hours
    sleep_hours = (
        db.query(func.coalesce(func.sum(DailyLog.sleep_hours), 0.0))
        .filter(DailyLog.user_id == user_id)
        .filter(DailyLog.date >= start_of_week)
        .filter(DailyLog.date <= today)
        .scalar()
    )

    # Sum workout distances
    distance_km_workouts = (
        db.query(func.coalesce(func.sum(Workout.distance_km), 0.0))
        .filter(Workout.user_id == user_id)
        .filter(Workout.log_date >= start_of_week)
        .filter(Workout.log_date <= today)
        .scalar()
    )

    return {
        "distance_km_suggested": round(distance_km_suggested, 2),
        "distance_km_workouts": round(distance_km_workouts, 2),
        "sleep_hours": round(sleep_hours, 2),
    }

from datetime import date, timedelta
from sqlalchemy.orm import Session
from models.sql_models import DailyLog, Workout


def get_last_n_days_logs_and_workouts(user_id: int, days: int, db: Session):
    today = date.today()
    start_date = today - timedelta(days=days - 1)

    logs = (
        db.query(DailyLog)
        .filter(DailyLog.user_id == user_id, DailyLog.date.between(start_date, today))
        .all()
    )

    workouts = (
        db.query(Workout)
        .filter(Workout.user_id == user_id, Workout.log_date.between(start_date, today))
        .all()
    )

    return logs, workouts


def build_weekly_dashboard_data(user_id: int, db: Session):
    logs, workouts = get_last_n_days_logs_and_workouts(user_id, 7, db)
    today = date.today()
    week_ago = today - timedelta(days=6)

    day_data = []
    for i in range(7):
        d = week_ago + timedelta(days=i)
        workout = next((w for w in workouts if w.log_date == d), None)
        day_data.append(
            {
                "day": d.strftime("%A"),
                "date": d.strftime("%m/%d"),
                "completed": workout is not None,
                "expectedCalories": 0,
            }
        )

    workout_data = [
        {
            "date": w.log_date.isoformat(),
            "type": w.type,
            "duration": w.duration_minutes,
            "calories": 0,
            "description": w.description,
            "summary": "Generated summary here",
        }
        for w in workouts
    ]

    return {"days": day_data, "entries": workout_data}


def build_user_history(user_id: int, db: Session):
    logs, workouts = get_last_n_days_logs_and_workouts(user_id, 90, db)

    summary_data = []
    for log in logs:
        matching_workouts = [w for w in workouts if w.log_date == log.date]
        total_minutes = sum(w.duration_minutes for w in matching_workouts)
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
            "calories": 0,
            "description": w.description,
            "summary": "Generated summary placeholder",
        }
        for w in workouts
    ]

    return {"summary": summary_data, "entries": workout_entries}

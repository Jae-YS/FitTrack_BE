from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.models.sql_models import DailyLog, Workout


def get_weekly_summary(user_id: int, db: Session) -> list[dict]:
    today = date.today()
    one_week_ago = today - timedelta(days=6)

    results = (
        db.query(
            DailyLog.date.label("date"),
            DailyLog.sleep_hours.label("sleep_hours"),
            func.coalesce(func.sum(Workout.duration_minutes), 0).label(
                "total_workout_minutes"
            ),
        )
        .outerjoin(
            Workout,
            (Workout.user_id == DailyLog.user_id) & (Workout.log_date == DailyLog.date),
        )
        .filter(DailyLog.user_id == user_id)
        .filter(DailyLog.date >= one_week_ago)
        .group_by(DailyLog.date, DailyLog.sleep_hours)
        .order_by(DailyLog.date.desc())
        .all()
    )

    return [
        {
            "date": row.date.isoformat(),
            "sleep_hours": row.sleep_hours,
            "total_workout_minutes": row.total_workout_minutes,
        }
        for row in results
    ]

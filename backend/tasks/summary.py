from services.llm.summary_generator import generate_summary_from_logs
from models.sql_models import DailyLog
from sqlalchemy.orm import Session
from datetime import timedelta, date


async def trigger_summary_generation(user_id: str, db: Session):
    today = date.today()
    week_ago = today - timedelta(days=7)

    logs = (
        db.query(DailyLog)
        .filter(DailyLog.user_id == user_id, DailyLog.date >= week_ago)
        .all()
    )

    structured_logs = []
    for log in logs:
        structured_logs.append(
            {
                "date": log.date.isoformat(),
                "mood": log.mood,
                "sleep_hours": log.sleep_hours,
                "workout": (
                    ", ".join([w.type for w in log.workouts]) if log.workouts else None
                ),
            }
        )

    summary = await generate_summary_from_logs(user_id, structured_logs)

    print(summary)

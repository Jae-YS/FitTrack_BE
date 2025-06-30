from sqlalchemy.orm import Session
from backend.schemas import DailyLogCreate
from backend.db.models import DailyEntry


# Log a daily entry for a user
def log_entry(db: Session, entry_data: DailyLogCreate) -> DailyEntry:
    daily_log = DailyEntry(
        user_id=entry_data.user_id,
        date=entry_data.date,
        mood=entry_data.mood,
        sleep_hours=entry_data.sleep_hours,
    )
    db.add(daily_log)
    db.commit()
    db.refresh(daily_log)
    return daily_log

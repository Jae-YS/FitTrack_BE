from datetime import date
from backend.db.models import DailyEntry
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from backend.schemas.daily_entry_schema import DailyEntryCreate

from backend.services.logging_service import log_entry
from backend.db.session import get_db


router = APIRouter(prefix="/daily-entries", tags=["Daily Entries"])


# Check if today's daily entry already exists for the user
@router.get("/exists/{user_id}")
def check_daily_entry_exists(user_id: int, db: Session = Depends(get_db)):
    today = date.today()
    exists = (
        db.query(DailyEntry).filter_by(user_id=user_id, date=today).first() is not None
    )
    return {"exists": exists}


# Log a daily entry
@router.post("/entry", response_model=dict)
async def log_daily_entry(
    entry: DailyEntryCreate,
    db: Session = Depends(get_db),
):
    entry = log_entry(db, entry)
    return {"status": "logged", "user_id": entry.user_id, "date": entry.date}

# scripts/reset_db.py
import sys
import os
import psycopg2

print(psycopg2.__version__)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import date, timedelta
from sqlalchemy.orm import Session
from backend.db.session import SessionLocal, engine
from backend.models.sql_models import Base, User, DailyLog, Workout


def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    try:
        # Create test user
        user = User(
            email="mockuser@example.com",
            name="Mock User",
            height=70.0,
            weight=160.0,
            sex="male",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        today = date.today()
        for i in range(14):  # last 14 days
            log_date = today - timedelta(days=i)
            log = DailyLog(
                user_id=user.id,
                date=log_date,
                mood=str(6 + (i % 4)),  # mood cycles 6-9
                sleep_hours=6.0 + (i % 3),  # sleep 6–8 hrs
            )
            db.add(log)

            if i % 2 == 0:  # every other day, add a workout
                workout = Workout(
                    user_id=user.id,
                    log_date=log_date,
                    type="Cardio" if i % 4 == 0 else "Strength",
                    description="Mock workout",
                    duration_minutes=30 + (i * 2),
                )
                db.add(workout)

        db.commit()
        print("✅ Database reset and populated with mock data.")

    finally:
        db.close()


if __name__ == "__main__":
    reset_db()

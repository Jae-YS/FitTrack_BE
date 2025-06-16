from datetime import date, timedelta
from sqlalchemy.orm import Session
from db.session import SessionLocal, engine
from models.sql_models import Base, User, DailyLog, Workout
from core.security import hash_password

# Predefined workout schedule
WORKOUT_PLAN = [
    ("easy", "Easy shakeout run", 40, 6.0, "easy"),
    ("strength", "Strength training (upper body)", 45, None, "moderate"),
    ("tempo", "Tempo run", 50, 8.0, "hard"),
    ("recovery", "Recovery bike ride", 30, None, "easy"),
    ("long", "Long run", 90, 15.0, "moderate"),
    ("cross-training", "Yoga session", 45, None, "easy"),
    ("rest", "", None, None, None),  # rest day (no workout)
]


def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    try:
        # Create test user
        user = User(
            email="mockuser@example.com",
            hashed_password=hash_password("password123"),
            name="Mock User",
            height=70.0,
            weight=160.0,
            sex="male",
            race_date=date.today() + timedelta(days=45),
            race_level="intermediate",
            pr_5k=25.5,
            pr_10k=55.0,
            pr_half=None,
            pr_full=None,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        today = date.today()

        for i in range(14):  # past 14 days
            log_date = today - timedelta(days=i)

            log = DailyLog(
                user_id=user.id,
                date=log_date,
                mood=str(5 + (i % 5)),  # 5–9 mood
                sleep_hours=6.0 + (i % 3),  # 6–8 hrs sleep
            )
            db.add(log)

            # Simulate rotating training pattern
            workout_plan = WORKOUT_PLAN[i % len(WORKOUT_PLAN)]
            workout_type, desc, duration, distance, effort = workout_plan

            if workout_type != "rest":
                workout = Workout(
                    user_id=user.id,
                    log_date=log_date,
                    type=workout_type,
                    description=desc,
                    duration_minutes=duration,
                    distance_km=distance,
                    effort_level=effort,
                )
                db.add(workout)

        db.commit()
        print("Database reset and populated with realistic mock training data.")

    finally:
        db.close()


if __name__ == "__main__":
    reset_db()

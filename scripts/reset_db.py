from datetime import date, timedelta
from sqlalchemy.orm import Session
from backend.db.session import SessionLocal
from backend.models.sql_models import User, DailyLog, Workout
from backend.core.security import hash_password
from backend.services.calories import calculate_calories

# Predefined workout plan: (type, description, duration (min), distance (km), effort level)
WORKOUT_PLAN = [
    ("easy", "Easy shakeout run", 40, 6.0, "easy"),
    ("strength", "Strength training (upper body)", 45, None, "moderate"),
    ("tempo", "Tempo run", 50, 8.0, "hard"),
    ("recovery", "Recovery bike ride", 30, None, "easy"),
    ("long", "Long run", 90, 15.0, "moderate"),
    ("cross-training", "Yoga session", 45, None, "easy"),
    ("rest", "", None, None, None),
]


def seed_mock_user_and_logs(db: Session):
    user = User(
        email="mockuser@example.com",
        hashed_password=hash_password("password123"),
        name="Mock User",
        height=185,  # cm
        weight=72.6,  # kg
        sex="male",
        race_type="half_marathon",
        race_level="intermediate",
        race_date=date.today() + timedelta(days=45),
        pr_5k=25.5,
        pr_10k=55.0,
        pr_half=None,
        pr_full=None,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    today = date.today()

    for i in range(14):  # Generate logs for past 14 days
        log_date = today - timedelta(days=i)

        log = DailyLog(
            user_id=user.id,
            date=log_date,
            mood=str(5 + (i % 5)),  # mood: 5–9
            sleep_hours=6.0 + (i % 3),  # sleep: 6–8 hrs
        )
        db.add(log)

        workout_type, desc, duration, distance, effort = WORKOUT_PLAN[
            i % len(WORKOUT_PLAN)
        ]

        if workout_type != "rest":
            calories = calculate_calories(workout_type, duration, user.weight)
            workout = Workout(
                user_id=user.id,
                log_date=log_date,
                type=workout_type,
                description=desc,
                duration_minutes=duration,
                distance_km=distance,
                effort_level=effort,
                calories_burned=round(calories, 2),
            )
            db.add(workout)

    db.commit()
    print("Mock user and workout logs seeded successfully.")


def reset_db():
    db: Session = SessionLocal()
    try:
        # WARNING: This assumes Alembic has already created your schema!
        db.query(Workout).delete()
        db.query(DailyLog).delete()
        db.query(User).delete()
        db.commit()

        seed_mock_user_and_logs(db)
    finally:
        db.close()


if __name__ == "__main__":
    reset_db()

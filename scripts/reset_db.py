from datetime import date, timedelta
from sqlalchemy.orm import Session
from backend.db.session import SessionLocal
from backend.db.models import User, DailyEntry, CompletedWorkout, RacePlan, PersonalBest
from backend.core.security import hash_password

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
        height_cm=185,
        sex="male",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Seed personal bests
    prs = [
        PersonalBest(user_id=user.id, distance_type="5k", time_minutes=25.5),
        PersonalBest(user_id=user.id, distance_type="10k", time_minutes=55.0),
    ]
    db.add_all(prs)

    # Seed race plan
    race = RacePlan(
        user_id=user.id,
        race_type="half_marathon",
        race_date=date.today() + timedelta(days=45),
        target_level="intermediate",
        notes="Mock plan",
    )
    db.add(race)

    today = date.today()

    for i in range(14):  # Generate logs for past 14 days
        log_date = today - timedelta(days=i)

        log = DailyEntry(
            user_id=user.id,
            date=log_date,
            mood=str(5 + (i % 5)),
            sleep_hours=6.0 + (i % 3),
        )
        db.add(log)

        workout_type, desc, duration, distance, effort = WORKOUT_PLAN[
            i % len(WORKOUT_PLAN)
        ]

        if workout_type != "rest":
            workout = CompletedWorkout(
                user_id=user.id,
                date=log_date,
                workout_type=workout_type,
                description=desc,
                duration_minutes=duration,
                distance_km=distance,
                effort_level=effort,
                planned_workout_id=None,
            )
            db.add(workout)

    db.commit()
    print("Mock user and workout logs seeded successfully.")


def reset_db():
    db: Session = SessionLocal()
    try:
        db.query(CompletedWorkout).delete()
        db.query(DailyEntry).delete()
        db.query(RacePlan).delete()
        db.query(PersonalBest).delete()
        db.query(User).delete()
        db.commit()

        seed_mock_user_and_logs(db)
    finally:
        db.close()


if __name__ == "__main__":
    reset_db()

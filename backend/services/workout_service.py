from datetime import date, timedelta


from backend.models.sql_models import SuggestedWorkout, Workout
from sqlalchemy.orm import Session

from backend.services.llm.format.parse_suggestions import parse_suggestions
from backend.services.llm.workout_generator import generate_next_week_plan


def get_workouts(user_id: int, db: Session):
    today = date.today()
    days_since_sunday = today.weekday() + 1
    past_sunday = today - timedelta(days=days_since_sunday % 7)

    return (
        db.query(SuggestedWorkout)
        .filter(
            SuggestedWorkout.user_id == user_id,
            SuggestedWorkout.recommended_date >= past_sunday,
        )
        .order_by(SuggestedWorkout.recommended_date.desc())  # newest first
        .limit(7)
        .all()
    )


async def get_next_workout(user_id: int, db: Session):
    today = date.today()
    if today.weekday() != 6:
        return None

    recent_workouts = (
        db.query(Workout)
        .filter(Workout.user_id == user_id)
        .order_by(Workout.log_date.desc())
        .all()
    )
    user = db.query(Workout).filter(Workout.user_id == user_id).all()

    existing = (
        db.query(SuggestedWorkout)
        .filter(
            SuggestedWorkout.user_id == user_id,
            SuggestedWorkout.recommended_date == today,
        )
        .first()
    )

    if existing:
        return None

    suggested_workout_past = (
        db.query(SuggestedWorkout)
        .filter(SuggestedWorkout.user_id == user_id)
        .order_by(SuggestedWorkout.recommended_date.desc())
        .first()
    )

    plan_text = await generate_next_week_plan(
        race_type=user.race_type,
        race_day=user.race_day,
        level=user.level,
        week_number=suggested_workout_past.week + 1,
        recent_workouts=recent_workouts,
    )

    print(f"Generated plan for week {suggested_workout_past.week + 1}: {plan_text}")

    suggestions = parse_suggestions(
        plan_text,
        user_id=user.id,
        week=suggested_workout_past.week + 1,
        base_date=today,
    )

    print("added suggestions:")

    for suggestion in suggestions:
        db.add(suggestion)

    db.commit()
    return user

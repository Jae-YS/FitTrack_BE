from datetime import datetime, timezone

from fastapi import HTTPException
from backend.models.sql_models import SuggestedWorkout, Workout
from sqlalchemy.orm import Session

from backend.services.llm.format.parse_suggestions import parse_suggestions
from backend.services.llm.workout_generator import generate_next_week_plan


def get_workouts(user_id: int, db: Session):

    return (
        db.query(SuggestedWorkout)
        .filter(SuggestedWorkout.user_id == user_id)
        .order_by(SuggestedWorkout.recommended_date.asc())
        .all()
    )


async def get_next_workout(user_id: int, db: Session):
    today = datetime.now(timezone.utc).date()
    if today.weekday() != 6:
        raise HTTPException(
            status_code=403, detail="This operation is only allowed on Sundays."
        )

    recent_workouts = (
        db.query(Workout)
        .filter(Workout.user_id == user_id)
        .order_by(Workout.log_date.desc())
        .all()
    )
    user = db.query(Workout).filter(Workout.user_id == user_id).all()

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

    print(plan_text)

    suggestions = parse_suggestions(
        plan_text,
        user_id=user.id,
        week=suggested_workout_past.week + 1,
        base_date=today,
    )

    for suggestion in suggestions:
        db.add(suggestion)

    db.commit()
    return user

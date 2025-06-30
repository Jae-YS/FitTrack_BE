from datetime import date, timedelta

from fastapi import HTTPException


from backend.db.models import CompletedWorkout, PlannedWorkout, TrainingPlan, RacePlan
from backend.schemas.completed_workout_schema import CompletedWorkoutCreate
from sqlalchemy.orm import Session

from backend.services.llm.format.parse_suggestions import parse_suggestions
from backend.services.llm.workout_generator import generate_next_week_plan


# Generate a weekly training plan for a user based on their
def get_workouts(user_id: int, db: Session):
    today = date.today()
    days_since_sunday = (today.weekday() + 1) % 7
    past_sunday = today - timedelta(days=days_since_sunday)

    print(f"Fetching workouts for user {user_id} since past Sunday: {past_sunday}")

    return (
        db.query(PlannedWorkout)
        .filter(
            PlannedWorkout.user_id == user_id,
            PlannedWorkout.recommended_date >= past_sunday,
        )
        .order_by(PlannedWorkout.recommended_date.asc())
        .limit(7)
        .all()
    )


# Generate the next training plan for a user
async def generate_next_training_plan(user_id: int, db: Session):
    today = date.today()
    if today.weekday() != 6:  # Only run on Sunday
        return None

    if _training_plan_exists_for_today(user_id, today, db):
        return None

    recent_workouts = _get_recent_workouts(user_id, db)
    last_week = _get_last_training_plan_week(user_id, today, db)
    race_plan = _get_upcoming_race_plan(user_id, today, db)

    plan_text = await generate_next_week_plan(
        race_type=race_plan.race_type,
        race_day=race_plan.race_date,
        level=race_plan.target_level,
        week_number=last_week + 1,
        recent_workouts=recent_workouts,
    )

    new_training_plan = parse_suggestions(
        plan_text,
        user_id=user_id,
        week=last_week + 1,
        base_date=today,
    )

    for planned_workout in new_training_plan:
        db.add(planned_workout)

    db.commit()
    return new_training_plan


def _training_plan_exists_for_today(user_id: int, today: date, db: Session) -> bool:
    existing = (
        db.query(TrainingPlan)
        .filter(
            TrainingPlan.user_id == user_id,
            TrainingPlan.recommended_date == today,
        )
        .first()
    )
    return existing is not None


def _get_recent_workouts(user_id: int, db: Session):
    three_weeks_ago = date.today() - timedelta(weeks=3)
    return (
        db.query(CompletedWorkout)
        .filter(
            CompletedWorkout.user_id == user_id,
            CompletedWorkout.date >= three_weeks_ago,
        )
        .order_by(CompletedWorkout.date.desc())
        .all()
    )


def _get_last_training_plan_week(user_id: int, today: date, db: Session) -> int:
    last_plan = (
        db.query(TrainingPlan)
        .filter(
            TrainingPlan.user_id == user_id,
            TrainingPlan.recommended_date < today,
        )
        .order_by(TrainingPlan.recommended_date.desc())
        .first()
    )
    return last_plan.week if last_plan else 0


def _get_upcoming_race_plan(user_id: int, today: date, db: Session):
    race_plan = (
        db.query(RacePlan)
        .filter(RacePlan.user_id == user_id, RacePlan.race_date >= today)
        .order_by(RacePlan.race_date.asc())
        .first()
    )

    if not race_plan:
        raise HTTPException(status_code=404, detail="No upcoming race plan found")

    return race_plan

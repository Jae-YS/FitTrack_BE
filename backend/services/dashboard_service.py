from collections import defaultdict
from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.db.models import CompletedWorkout, DailyEntry, TrainingPlan


def _get_previous_sunday(today: date) -> date:
    return today - timedelta(days=today.weekday() + 1 if today.weekday() != 6 else 0)


def _get_entries_and_workouts(
    user_id: int, start_date: date, end_date: date, db: Session
):
    entries = (
        db.query(DailyEntry)
        .filter(
            DailyEntry.user_id == user_id,
            DailyEntry.date.between(start_date, end_date),
        )
        .all()
    )

    workouts = (
        db.query(CompletedWorkout)
        .filter(
            CompletedWorkout.user_id == user_id,
            CompletedWorkout.log_date.between(start_date, end_date),
        )
        .all()
    )

    return entries, workouts


# Build the workout history for a user
def build_workout_history(user_id: int, db: Session):
    today = date.today()
    start_date = today - timedelta(days=55)
    entries, workouts = _get_entries_and_workouts(user_id, start_date, today, db)

    workouts_by_date = defaultdict(list)
    for workout in workouts:
        workouts_by_date[workout.log_date].append(workout)

    summary_data = [
        {
            "date": entry.date.isoformat(),
            "sleep_hours": entry.sleep_hours,
            "total_workout_minutes": sum(
                w.duration_minutes
                for w in workouts_by_date.get(entry.date, [])
                if w.duration_minutes
            ),
        }
        for entry in entries
    ]

    workout_entries = [
        {
            "date": workout.log_date.isoformat(),
            "type": workout.type,
            "duration": workout.duration_minutes,
            "description": workout.description,
            "summary": "Generated summary placeholder",
        }
        for workout in workouts
    ]

    return {
        "summary": summary_data,
        "entries": workout_entries,
    }


# Build the weekly dashboard data for a user
def build_weekly_dashboard_data(user_id: int, db: Session):
    today = date.today()
    last_sunday = _get_previous_sunday(today)
    week_end = last_sunday + timedelta(days=6)

    _, workouts = _get_entries_and_workouts(user_id, last_sunday, week_end, db)

    workouts_by_date = defaultdict(list)
    for workout in workouts:
        workouts_by_date[workout.log_date].append(workout)

    day_data = []
    for i in range(7):
        current_date = last_sunday + timedelta(days=i)
        workouts_today = workouts_by_date.get(current_date, [])

        day_data.append(
            {
                "day": current_date.strftime("%A"),
                "date": current_date.strftime("%m/%d"),
                "completed": bool(workouts_today),
                "workouts": [
                    {
                        "type": workout.type,
                        "durationMinutes": workout.duration_minutes,
                        "distancekm": workout.distance_km,
                    }
                    for workout in workouts_today
                ],
            }
        )

    workout_data = [
        {
            "date": workout.log_date.isoformat(),
            "type": workout.type,
            "duration": workout.duration_minutes,
            "description": workout.description,
            "summary": "Generated summary here",
        }
        for workout in workouts
    ]

    return {
        "days": day_data,
        "entries": workout_data,
    }


#
def get_weekly_progress_data(user_id: int, db: Session) -> dict:
    today = date.today()
    start_of_week = _get_previous_sunday(today)

    training_plan_distance = (
        db.query(TrainingPlan.total_distance_km)
        .filter(TrainingPlan.user_id == user_id)
        .scalar()
        or 0.0
    )

    hours_slept = (
        db.query(func.coalesce(func.sum(DailyEntry.sleep_hours), 0.0))
        .filter(
            DailyEntry.user_id == user_id,
            DailyEntry.date >= start_of_week,
            DailyEntry.date <= today,
        )
        .scalar()
    )

    distance_km_workouts = (
        db.query(func.coalesce(func.sum(CompletedWorkout.distance_km), 0.0))
        .filter(
            CompletedWorkout.user_id == user_id,
            CompletedWorkout.log_date >= start_of_week,
            CompletedWorkout.log_date <= today,
        )
        .scalar()
    )

    return {
        "distance_km_suggested": round(training_plan_distance, 2),
        "distance_km_workouts": round(distance_km_workouts, 2),
        "sleep_hours": round(hours_slept, 2),
    }

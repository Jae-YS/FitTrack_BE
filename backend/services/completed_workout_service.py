from requests import Session
from backend.db.models.completed_workout import CompletedWorkout
from backend.schemas.completed_workout_schema import CompletedWorkoutCreate


# Create a completed workout entry in the database
def create_completed_workout(db: Session, data: CompletedWorkoutCreate):
    workout = CompletedWorkout(**data.model_dump())
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout

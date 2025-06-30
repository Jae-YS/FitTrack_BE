from sqlalchemy import Integer, String, Float, Date, ForeignKey, Column
from sqlalchemy.orm import relationship
from backend.db.session import Base


class PlannedWorkout(Base):
    __tablename__ = "planned_workouts"

    id = Column(Integer, primary_key=True)
    training_plan_id = Column(
        Integer, ForeignKey("training_plans.id", ondelete="CASCADE")
    )
    recommended_date = Column(Date)
    workout_type = Column(String, nullable=False)
    description = Column(String)
    duration_minutes = Column(Integer)
    distance_km = Column(Float, nullable=True)
    pace = Column(String, nullable=True)

    training_plan = relationship("TrainingPlan", back_populates="planned_workouts")
    completed_workout = relationship(
        "CompletedWorkout", back_populates="planned_workout", uselist=False
    )

    def __repr__(self):
        return (
            f"<PlannedWorkout(id={self.id}, training_plan_id={self.training_plan_id}, "
            f"recommended_date={self.recommended_date}, workout_type={self.workout_type}, "
            f"description={self.description}, duration_minutes={self.duration_minutes}, "
            f"distance_km={self.distance_km}, pace={self.pace})>"
        )

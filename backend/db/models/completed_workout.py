from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Float,
    Date,
)
from sqlalchemy.orm import relationship
from backend.db.session import Base


class CompletedWorkout(Base):
    __tablename__ = "completed_workouts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    date = Column(Date, nullable=False)

    workout_type = Column(String, nullable=False)
    description = Column(String, nullable=True)
    duration_minutes = Column(Integer)
    distance_km = Column(Float)
    pace_min_per_km = Column(Float)
    effort_level = Column(String)

    planned_workout_id = Column(
        Integer, ForeignKey("planned_workouts.id", ondelete="SET NULL"), nullable=True
    )

    user = relationship("User", back_populates="completed_workouts")
    planned_workout = relationship("PlannedWorkout", back_populates="completed_workout")

    def __repr__(self):
        return (
            f"<CompletedWorkout(id={self.id}, user_id={self.user_id}, date={self.date}, "
            f"workout_type={self.workout_type}, description={self.description}, "
            f"duration_minutes={self.duration_minutes}, distance_km={self.distance_km}, "
            f"pace_min_per_km={self.pace_min_per_km}, effort_level={self.effort_level})>"
        )

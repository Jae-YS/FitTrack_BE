from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.db.session import Base


class TrainingPlan(Base):
    __tablename__ = "training_plans"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    week = Column(Integer, nullable=False)
    goal = Column(String, nullable=True)
    focus = Column(String, nullable=True)
    total_distance_km = Column(Integer, nullable=True)
    intensity = Column(String, nullable=True)

    user = relationship("User", back_populates="training_plans")
    planned_workouts = relationship(
        "PlannedWorkout", back_populates="training_plan", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<TrainingPlan(id={self.id}, user_id={self.user_id}, week={self.week}, "
            f"goal={self.goal}, focus={self.focus}, intensity={self.intensity})>"
        )

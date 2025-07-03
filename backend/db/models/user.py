from sqlalchemy import Column, DateTime, Integer, String, Float, Date, func
from sqlalchemy.orm import relationship
from backend.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=True)
    height_cm = Column(Float, nullable=True)
    sex = Column(String, nullable=False)
    target_level = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    hashed_password = Column(String, nullable=False)

    # Relationships
    daily_entries = relationship(
        "DailyEntry", back_populates="user", cascade="all, delete-orphan"
    )
    training_plans = relationship(
        "TrainingPlan", back_populates="user", cascade="all, delete-orphan"
    )
    personal_bests = relationship(
        "PersonalBest", back_populates="user", cascade="all, delete-orphan"
    )
    race_plans = relationship(
        "RacePlan", back_populates="user", cascade="all, delete-orphan"
    )
    completed_workouts = relationship(
        "CompletedWorkout", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<User(id={self.id}, email={self.email}, name={self.name}, "
            f"height_cm={self.height_cm}, sex={self.sex}, "
            f"created_at={self.created_at}, updated_at={self.updated_at})>"
        )

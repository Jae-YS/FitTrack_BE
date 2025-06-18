from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Float,
    Date,
    ForeignKey,
    ForeignKeyConstraint,
    Text,
)
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from backend.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    sex = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    race_date = Column(Date, nullable=True)
    race_type = Column(String, nullable=True)
    race_level = Column(String, nullable=True)
    pr_5k = Column(Float, nullable=True)
    pr_10k = Column(Float, nullable=True)
    pr_half = Column(Float, nullable=True)
    pr_full = Column(Float, nullable=True)

    logs = relationship("DailyLog", back_populates="user", cascade="all, delete-orphan")
    suggestions = relationship(
        "Suggestion", back_populates="user", cascade="all, delete-orphan"
    )


class DailyLog(Base):
    __tablename__ = "daily_logs"

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    date = Column(Date, primary_key=True)
    mood = Column(String, nullable=True)
    sleep_hours = Column(Float, nullable=True)

    user = relationship("User", back_populates="logs")
    workouts = relationship(
        "Workout", back_populates="daily_log", cascade="all, delete-orphan"
    )


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    log_date = Column(Date, index=True)

    type = Column(String, nullable=False)
    description = Column(String, nullable=True)
    duration_minutes = Column(Integer, nullable=True)

    distance_km = Column(Float, nullable=True)
    pace_min_per_km = Column(Float, nullable=True)
    effort_level = Column(String, nullable=True)

    calories_burned = Column(Float, nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id", "log_date"],
            ["daily_logs.user_id", "daily_logs.date"],
            ondelete="CASCADE",
        ),
    )

    summary = relationship(
        "Summary", back_populates="workout", uselist=False, cascade="all, delete-orphan"
    )
    daily_log = relationship("DailyLog", back_populates="workouts")


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(
        Integer, ForeignKey("workouts.id", ondelete="CASCADE"), unique=True
    )
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    workout = relationship("Workout", back_populates="summary")


class Suggestion(Base):
    __tablename__ = "suggestions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    content = Column(Text, nullable=False)
    week_start = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="suggestions")


class SuggestedWorkout(Base):
    __tablename__ = "suggested_workouts"

    id = Column(Integer, primary_key=True, index=True)
    week = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    recommended_date = Column(Date)
    workout_type = Column(String, nullable=False)
    description = Column(String)
    duration_minutes = Column(Integer)
    distance_km = Column(Float, nullable=True)
    focus = Column(String, nullable=True)
    pace = Column(String, nullable=True)
    goal = Column(String, nullable=True)
    intensity = Column(String, nullable=True)

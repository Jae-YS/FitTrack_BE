from sqlalchemy import (
    ForeignKey,
    Column,
    Integer,
    String,
    Float,
    Date,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from backend.db.session import Base


class DailyEntry(Base):
    __tablename__ = "daily_entries"

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    date = Column(Date, primary_key=True)

    mood = Column(String, nullable=True)
    sleep_hours = Column(Float, nullable=True)

    user = relationship("User", back_populates="daily_entries")

    __table_args__ = (UniqueConstraint("user_id", "date", name="uix_user_date"),)

    def __repr__(self):
        return (
            f"<DailyEntry(user_id={self.user_id}, date={self.date}, "
            f"mood={self.mood}, sleep_hours={self.sleep_hours})>"
        )

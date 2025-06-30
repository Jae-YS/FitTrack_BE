from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.db.session import Base


class PersonalBest(Base):
    __tablename__ = "personal_bests"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    distance_type = Column(String, nullable=False)
    time_minutes = Column(Float, nullable=False)
    recorded_date = Column(Date, nullable=True)

    user = relationship("User", back_populates="personal_bests")

    def __repr__(self):
        return (
            f"<PersonalBest(id={self.id}, user_id={self.user_id}, "
            f"distance_type={self.distance_type}, time_minutes={self.time_minutes}, "
            f"recorded_date={self.recorded_date})>"
        )

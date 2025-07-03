from sqlalchemy import Integer, String, Date, ForeignKey, Column
from sqlalchemy.orm import relationship
from backend.db.session import Base


class RacePlan(Base):
    __tablename__ = "race_plans"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    race_type = Column(String, nullable=False)
    race_date = Column(Date, nullable=False)
    notes = Column(String, nullable=True)

    user = relationship("User", back_populates="race_plans")

    def __repr__(self):
        return (
            f"<RacePlan(id={self.id}, user_id={self.user_id}, "
            f"race_type={self.race_type}, race_date={self.race_date}, "
            f"notes={self.notes})>"
        )

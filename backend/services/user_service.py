# services/user_service.py
from sqlalchemy.orm import Session
from models.sql_models import User
from models.schemas import UserCreate


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter_by(email=email).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter_by(id=user_id).first()


def create_user(db: Session, user_data: UserCreate) -> User:
    new_user = User(**user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

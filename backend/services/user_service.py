from sqlalchemy.orm import Session
from models.sql_models import User
from models.schemas import UserCreate
from core.security import hash_password, verify_password


def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter_by(email=email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter_by(id=user_id).first()


def create_user(db: Session, user_data: UserCreate) -> User:
    user_dict = user_data.dict()
    raw_password = user_dict.pop("password")
    user_dict["hashed_password"] = hash_password(raw_password)

    new_user = User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

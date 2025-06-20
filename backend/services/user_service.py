from backend.services.llm.format.parse_suggestions import parse_suggestions
from sqlalchemy.orm import Session
from backend.models.sql_models import User
from backend.models.schemas import UserCreate
from backend.core.security import hash_password, verify_password
from backend.services.llm.workout_generator import generate_first_week_plan
from datetime import date, datetime, timezone


def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter_by(email=email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter_by(id=user_id).first()


async def create_user(db: Session, user_data: UserCreate) -> User:
    user_dict = user_data.model_dump()
    raw_password = user_dict.pop("password")
    user_dict["hashed_password"] = hash_password(raw_password)

    new_user = User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    today_date = date.today()

    plan_text = await generate_first_week_plan(
        race_type=new_user.race_type,
        race_day=str(new_user.race_date),
        level=new_user.race_level,
        today=date.today().isoformat(),
        today_str=today_date.isoformat(),
        today_day=today_date.strftime("%A"),
        pr_5k=new_user.pr_5k,
        pr_10k=new_user.pr_10k,
        pr_half=new_user.pr_half,
        pr_full=new_user.pr_full,
    )

    today = datetime.now(timezone.utc).date()

    suggestions = parse_suggestions(
        plan_text,
        user_id=new_user.id,
        week=1,  # First workout week once you create a user
        base_date=today,
    )

    for suggestion in suggestions:
        db.add(suggestion)

    db.commit()
    return new_user

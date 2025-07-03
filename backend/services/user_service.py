from fastapi import HTTPException
from backend.db.models.personal_best import PersonalBest
from backend.db.models.race_plan import RacePlan
from backend.db.models.training_plan import TrainingPlan
from backend.services.llm.format.parse_suggestions import (
    extract_plan_metadata,
    parse_suggestions,
)
from sqlalchemy.orm import Session
from backend.db.models import User
from backend.schemas import UserCreate
from backend.core.security import hash_password, verify_password
from backend.services.llm.workout_generator import generate_first_week_plan
from datetime import date, datetime, timezone


# User authentication and management service
def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter_by(email=email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


# Get a user by their ID
def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter_by(id=user_id).first()


# Get a user by their email
async def register_user(db: Session, user_data: UserCreate) -> User:
    existing_user = db.query(User).filter_by(email=user_data.email).first()
    if existing_user:
        raise ValueError("User with this email already exists")
    print(f"Creating user with email: {user_data.email}")
    return await create_user(db, user_data)


# Create a new user in the database
async def create_user(db: Session, user_data: UserCreate) -> User:
    user_dict = user_data.model_dump()
    print(f"Creating user with data: {user_dict}")

    personal_bests_data = user_dict.pop("personal_bests", [])
    race_plans_data = user_dict.pop("race_plans", [])

    raw_password = user_dict.pop("password")
    user_dict["hashed_password"] = hash_password(raw_password)

    new_user = User(**user_dict)
    db.add(new_user)
    db.flush()

    _add_personal_bests(db, new_user.id, personal_bests_data)
    _add_race_plans(db, new_user.id, race_plans_data)

    _generate_initial_training_plan(db, new_user)

    db.commit()
    return new_user


def _add_personal_bests(db: Session, user_id: int, personal_bests_data):
    for pb in personal_bests_data:
        new_pb = PersonalBest(user_id=user_id, **pb)
        db.add(new_pb)


def _add_race_plans(db: Session, user_id: int, race_plans_data):
    for rp in race_plans_data:
        new_rp = RacePlan(user_id=user_id, **rp)
        db.add(new_rp)


async def _generate_initial_training_plan(db: Session, new_user: User):
    today_date = date.today()

    if not new_user.race_plans:
        raise HTTPException(
            status_code=400, detail="No race plan available to generate suggestions."
        )

    race_plan = new_user.race_plans[0]
    pr_lookup = {
        pb.distance_type.lower(): pb.time_minutes for pb in new_user.personal_bests
    }

    plan_text = await generate_first_week_plan(
        race_type=race_plan.race_type,
        race_day=str(race_plan.race_date),
        level=new_user.target_level,
        today_str=today_date.isoformat(),
        today_day=today_date.strftime("%A"),
        pr_5k=pr_lookup.get("5k"),
        pr_10k=pr_lookup.get("10k"),
        pr_half=pr_lookup.get("half"),
        pr_full=pr_lookup.get("full"),
    )

    focus, goal, intensity, distance = extract_plan_metadata(plan_text)

    training_plan = TrainingPlan(
        user_id=new_user.id,
        week=1,
        goal=goal,
        focus=focus,
        total_distance_km=distance,
        intensity=intensity,
    )

    db.add(training_plan)
    db.flush()

    suggestions = parse_suggestions(
        plan_text,
        training_plan_id=training_plan.id,
        base_date=datetime.now(timezone.utc).date(),
    )

    for suggestion in suggestions:
        db.add(suggestion)

    return


def get_race_date(user: User) -> date | None:

    user.race_plans.sort(key=lambda rp: rp.race_date)
    return user.race_plans[0].race_date if user.race_plans else None

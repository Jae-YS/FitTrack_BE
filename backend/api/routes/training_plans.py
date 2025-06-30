from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.schemas.training_plan_schema import (
    TrainingPlanRequest,
    TrainingPlanResponse,
)
from backend.services.workout_service import (
    generate_next_training_plan,
)

router = APIRouter(prefix="/training-plans", tags=["Training Plans"])


# Generate the next training plan for a user
@router.post("/get-next-training-plan", response_model=TrainingPlanResponse)
async def generate_next_training_plan(
    request_data: TrainingPlanRequest,
    db: Session = Depends(get_db),
):
    user_id = request_data.user_id

    new_plan = await generate_next_training_plan(db, user_id)
    return new_plan

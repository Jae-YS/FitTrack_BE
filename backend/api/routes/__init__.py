from fastapi import APIRouter
from backend.api.routes import (
    users,
    daily_entries,
    route_planner,
    training_plans,
    completed_workouts,
    dashboard,
)

router = APIRouter()
router.include_router(users.router)
router.include_router(daily_entries.router)
router.include_router(route_planner.router)
router.include_router(training_plans.router)
router.include_router(completed_workouts.router)
router.include_router(dashboard.router)

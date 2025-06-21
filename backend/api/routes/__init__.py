from fastapi import APIRouter
from backend.api.routes import users, logs, suggestions, route_planner

router = APIRouter()
router.include_router(users.router)
router.include_router(logs.router)
router.include_router(suggestions.router)
router.include_router(route_planner.router)

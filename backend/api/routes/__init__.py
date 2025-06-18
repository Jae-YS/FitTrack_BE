from fastapi import APIRouter
from backend.api.routes import users, logs, suggestions

router = APIRouter()
router.include_router(users.router)
router.include_router(logs.router)
router.include_router(suggestions.router)

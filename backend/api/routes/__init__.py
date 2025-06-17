from fastapi import APIRouter
from backend.api.routes import users, logs

router = APIRouter()
router.include_router(users.router)
router.include_router(logs.router)

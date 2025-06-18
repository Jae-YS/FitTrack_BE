from backend.models.sql_models import User
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from backend.models.schemas.user_schema import UserCreate, UserOut
from backend.models.schemas.auth_schema import LoginRequest, LoginResponse
from backend.services.user_service import authenticate_user, get_user_by_id, create_user
from backend.db.session import get_db


router = APIRouter()


# Login user
@router.post("/login", response_model=LoginResponse)
def login(
    data: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    user = authenticate_user(data.email, data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    request.session["user_id"] = user.id

    return {"user": user, "is_new": False}


# Register new user
@router.post("/register", response_model=UserOut)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = await create_user(db, user)
    return new_user


# Get current user information
@router.get("/me")
def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not logged in")

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# Logout user
@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out"}

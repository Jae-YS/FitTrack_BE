from models.sql_models import User
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from models.schemas.user_schema import UserCreate, UserOut
from models.schemas.auth_schema import LoginRequest, LoginResponse
from services.user_service import authenticate_user, get_user_by_id, create_user
from db.session import get_db
from core.security import create_session_token


router = APIRouter()


@router.post("/login")
def login(data: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = authenticate_user(data.email, data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    response.set_cookie(
        key="session",
        value=create_session_token(user),
        httponly=True,
        samesite="Lax",  # or "None" if cross-origin
        secure=True,  # must be True in production with HTTPS
        max_age=60 * 60 * 24 * 7,
    )

    return {"user": user, "is_new": False}


@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = create_user(db, user)
    return new_user


@router.get("/me", response_model=UserOut)
def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not logged in")

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("session")
    return {"message": "Logged out"}

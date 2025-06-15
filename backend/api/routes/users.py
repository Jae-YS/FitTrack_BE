from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from models.schemas.user_schema import UserCreate, UserOut
from models.schemas.auth_schema import LoginRequest, LoginResponse
from services.user_service import get_user_by_email, get_user_by_id, create_user
from db.session import get_db

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    user = get_user_by_email(db, data.email)
    if user:
        request.session["user_id"] = user.id
        return {"user": user, "is_new": False}
    return {"user": None, "is_new": True}


@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    return create_user(db, user)


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
def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out"}

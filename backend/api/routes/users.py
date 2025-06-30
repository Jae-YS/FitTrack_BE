from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from backend.schemas.user_schema import UserCreate, UserResponse
from backend.schemas.auth_schema import LoginRequest, LoginResponse
from backend.services.user_service import (
    authenticate_user,
    get_user_by_id,
    register_user,
)
from backend.db.session import get_db


router = APIRouter(prefix="/users", tags=["Users"])


# Get current user information
@router.get("/me", response_model=UserResponse)
def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")

    if not user_id:
        raise HTTPException(status_code=401, detail="Not logged in")

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# Login user
@router.post("/login", response_model=LoginResponse)
def login_user(request: Request, data: LoginRequest, db: Session = Depends(get_db)):
    try:
        user = authenticate_user(data.email, data.password, db)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        request.session["user_id"] = user.id
        return user

    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error during login: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Register new user
@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = await register_user(db, user)
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        print(f"Register route crashed: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")


# Logout user
@router.post("/logout")
def logout(request: Request):
    if not request.session.get("user_id"):
        raise HTTPException(status_code=401, detail="Not logged in")
    request.session.clear()
    return {"message": "Logged out"}

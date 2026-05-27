from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.schemas import UserCreate, UserLogin, UserResponse, TokenResponse
from app.services.auth_service import register_user, login_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    - **full_name**: Your full name
    - **email**: Valid email address (must be unique)
    - **password**: Minimum 8 characters
    """
    return register_user(db, user_data)


@router.post("/login", response_model=TokenResponse)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login with email and password.

    Returns a **JWT token** — use this token to access protected routes.

    Add it to request headers as: `Authorization: Bearer <token>`
    """
    return login_user(db, login_data)

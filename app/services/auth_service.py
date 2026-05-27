from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.models import User
from app.schemas.schemas import UserCreate, UserLogin
from app.utils.password_utils import hash_password, verify_password
from app.utils.jwt_utils import create_access_token


def register_user(db: Session, user_data: UserCreate) -> User:
    """Register a new user. Raises error if email already exists."""

    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered. Please use a different email."
        )

    # Hash the password before saving
    hashed = hash_password(user_data.password)

    # Create new user object
    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        password=hashed
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def login_user(db: Session, login_data: UserLogin) -> dict:
    """Login user and return JWT token."""

    # Find user by email
    user = db.query(User).filter(User.email == login_data.email).first()

    # Check if user exists and password is correct
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create JWT token
    token = create_access_token(data={"sub": user.email})

    return {"access_token": token, "token_type": "bearer", "user": user}

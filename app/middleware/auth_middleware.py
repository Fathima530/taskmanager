from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.utils.jwt_utils import verify_access_token
from app.models.models import User

# Bearer token security
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current logged-in user."""

    # Extract token
    token = credentials.credentials

    # Verify JWT token
    payload = verify_access_token(token)

    # Extract email from token
    email = payload.get("sub")

    # Find user in database
    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user
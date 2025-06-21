# app/dependencies/auth.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.utils.jwt import verify_access_token  # Assuming this function verifies and decodes JWT
from app.models.user import User
from sqlalchemy.orm import Session
from app.dependencies import get_db  # Assuming you have a dependency to get DB session

# OAuth2PasswordBearer retrieves the token from the "Authorization" header as "Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Decode the token and get user info (this function should raise an exception if the token is invalid)
        user_email = verify_access_token(token)
        
        # Fetch user from the database using the decoded email (or other identifier)
        user = db.query(User).filter(User.email == user_email).first()
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

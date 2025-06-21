# app/utils/jwt.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status
from app.config import settings  # Assuming settings is configured to load the secret key from the environment

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Adjust the expiration time

def create_access_token(data: dict):
    """
    Creates a JWT token with the given data (usually user information), including an expiration time.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Set expiration time
    to_encode.update({"exp": expire})  # Add expiration claim to token

    # Sign the token using the secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    """
    Verifies a JWT token, checking for validity and decoding its contents.
    """
    try:
        # Attempt to decode the token
        print("Verifying token:", token)  # Debugging line to check the token
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[ALGORITHM])
        
        # Print the decoded payload to check its content (remove in production)
        print("Decoded payload:", payload)
        
        # Extract the 'sub' (subject), which is typically the user email or identifier
        user_email = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token does not contain user information")
        
        return user_email  # Return the user email (or other identifier, depending on your setup)
    
    except JWTError as e:
        # Catching general JWT decoding errors (invalid token, malformed token, etc.)
        print("JWTError exception:", str(e))  # Log the error for debugging purposes
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    except jwt.ExpiredSignatureError:
        # Handle expired token
        print("Token has expired.")  # Log for debugging
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")

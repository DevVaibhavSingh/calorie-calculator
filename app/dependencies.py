from app.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends

def get_db() -> Session:
    """
    Dependency that provides a database session for each request.
    It ensures that the session is closed properly after the request is finished.
    """
    db = SessionLocal()  # Create a new session using SessionLocal
    try:
        yield db  # Yield the session to the route handler
    finally:
        db.close()  # Close the session after the request is processed

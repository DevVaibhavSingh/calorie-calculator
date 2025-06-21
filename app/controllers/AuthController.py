# app/controllers/AuthController.py
from fastapi import APIRouter, HTTPException, Depends
from app.models.user import User
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.utils.security import hash_password, verify_password
from app.utils.jwt import create_access_token
from pydantic import EmailStr
from app.models.RegisterRequest import RegisterRequest
from app.models.LoginRequest import LoginRequest

router = APIRouter()

@router.post("/register")
async def register_user(user: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user by storing their first name, last name, email, and securely hashed password.
    """
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password
    hashed_password = hash_password(user.password)
    
    # Create new user
    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password_hash=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"msg": "User created successfully"}

@router.post("/login")
async def login_user(user: LoginRequest, db: Session = Depends(get_db)):
    """
    Log in a user by verifying their email and password.
    If valid, issue a JWT token.
    """
    # Find user by email
    user_record = db.query(User).filter(User.email == user.email).first()  # Use user.email instead of email
    
    if not user_record or not verify_password(user.password, user_record.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create JWT token
    from app.main import app  # Import inside function to avoid circular import
    access_token = create_access_token(data={"sub": user_record.email})
    
    return {"access_token": access_token, "token_type": "bearer", "user": user_record}

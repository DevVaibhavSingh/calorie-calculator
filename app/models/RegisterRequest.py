# app/schemas/user.py
from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

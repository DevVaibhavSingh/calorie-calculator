# app/models/user.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from app.models.base import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

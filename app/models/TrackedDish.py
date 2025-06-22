from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class TrackedDish(Base):
    __tablename__ = 'tracked_dishes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    dish_name = Column(String, nullable=False)
    servings = Column(Float, nullable=False)
    calories_per_serving = Column(Float, nullable=False)
    total_calories = Column(Float, nullable=False)
    source = Column(String, nullable=False)

    protein = Column(Float)
    carbs = Column(Float)
    fat = Column(Float)

    timestamp = Column(DateTime, default=datetime.utcnow)

    # Optional: backref to user
    user = relationship("User", backref="dishes")

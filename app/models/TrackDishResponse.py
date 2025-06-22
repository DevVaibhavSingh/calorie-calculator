from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TrackedDishResponse(BaseModel):
    id: int
    dish_name: str
    servings: float
    calories_per_serving: float
    total_calories: float
    source: str
    protein: Optional[float]
    carbs: Optional[float]
    fat: Optional[float]
    timestamp: datetime

    class Config:
        orm_mode = True

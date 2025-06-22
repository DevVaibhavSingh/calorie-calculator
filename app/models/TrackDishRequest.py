from pydantic import BaseModel
from typing import Optional

class TrackedDishRequest(BaseModel):
    dish_name: str
    servings: float
    calories_per_serving: float
    total_calories: float
    source: str
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None

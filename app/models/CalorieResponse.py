# app/models.py

from pydantic import BaseModel
from typing import Optional

class CalorieResponse(BaseModel):
    matched_dish_name: object
    dish_name: str
    servings: int
    calories_per_serving: float
    total_calories: float
    protein: Optional[float] = None
    fat: Optional[float] = None
    carbs: Optional[float] = None
    source: str
    cache: bool = None  # Indicates if the response was from cache
    success: bool = True  # Indicates if the request was successful

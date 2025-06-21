# app/models.py

from pydantic import BaseModel

class CalorieResponse(BaseModel):
    dish_name: str
    servings: int
    calories_per_serving: float
    total_calories: float
    source: str
    cache: bool = None  # Indicates if the response was from cache

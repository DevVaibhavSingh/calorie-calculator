
from pydantic import BaseModel

class CalorieRequest(BaseModel):
    dish_name: str
    servings: int
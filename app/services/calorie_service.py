# app/services/calorie_service.py

from app.models.CalorieRequest import CalorieRequest
from app.models.CalorieResponse import CalorieResponse
from app.services.dish import fetch_dish_data

async def get_calorie_info(request: CalorieRequest) -> CalorieResponse:
    if request.servings <= 0:
        raise ValueError("Servings must be greater than 0")

    # Pass both dish_name and servings to fetch_dish_data
    calories_per_serving = fetch_dish_data(request.dish_name, request.servings)
    total_calories = calories_per_serving * request.servings

    return CalorieResponse(
        dish_name=request.dish_name,
        servings=request.servings,
        calories_per_serving=calories_per_serving,
        total_calories=total_calories,
        source="USDA FoodData Center"
    )

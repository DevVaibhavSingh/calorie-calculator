from app.models.CalorieRequest import CalorieRequest
from app.models.CalorieResponse import CalorieResponse
from app.services.dish import fetch_dish_data

async def get_calorie_info(request: CalorieRequest) -> CalorieResponse:
    if request.servings <= 0:
        raise ValueError("Servings must be greater than 0")

    # Get full nutrient data as a dictionary
    nutrient_data = fetch_dish_data(request.dish_name, request.servings)

    return CalorieResponse(
        matched_dish_name= nutrient_data['matched_dish_name'],
        dish_name=request.dish_name,
        servings=request.servings,
        calories_per_serving=round(nutrient_data["calories"] / request.servings, 2),
        total_calories=nutrient_data["calories"],
        protein=nutrient_data.get("protein"),
        fat=nutrient_data.get("fat"),
        carbs=nutrient_data.get("carbs"),
        source="USDA FoodData Center"
    )

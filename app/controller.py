# # app/controllers.py

# from fastapi import APIRouter, HTTPException
# from app.models.CalorieRequest import CalorieRequest
# from app.models.CalorieResponse import CalorieResponse
# from .services import fetch_dish_data

# router = APIRouter()

# @router.post("/get-calories", response_model=CalorieResponse)
# async def get_calories(request: CalorieRequest):
#     # Validate the input
#     if request.servings <= 0:
#         raise HTTPException(status_code=400, detail="Servings must be greater than 0")
    
#     # Fetch data from USDA API
#     try:
#         calories_per_serving = fetch_dish_data(request.dish_name)
#         total_calories = calories_per_serving * request.servings
#     except HTTPException as e:
#         raise e
    
#     return CalorieResponse(
#         dish_name=request.dish_name,
#         servings=request.servings,
#         calories_per_serving=calories_per_serving,
#         total_calories=total_calories,
#         source="USDA FoodData Centrals"
#     )

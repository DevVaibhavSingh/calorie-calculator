# app/services.py

import requests
from fastapi import HTTPException
from app.config import Config

# Helper function to fetch data from USDA API and calculate calories based on servings
def fetch_dish_data(dish_name: str, servings: int):
    # Ensure servings is a positive number
    if servings <= 0:
        raise HTTPException(status_code=400, detail="Servings must be greater than 0")

    params = {
        'query': dish_name,
        'api_key': Config.API_KEY,
        'pageSize': 1  # Get the most relevant result
    }
    response = requests.get(Config.USDA_API_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching data from USDA API")
    
    data = response.json()
    if "foods" not in data or len(data["foods"]) == 0:
        raise HTTPException(status_code=404, detail="Dish not found")

    # Extract relevant food item
    food_item = data["foods"][0]
    
    # Default values in case specific fields are missing
    calories_per_serving = None
    calories_per_100g = None

    # Check if calories per serving is available
    for nutrient in food_item["foodNutrients"]:
        if nutrient["nutrientName"] == "Energy" and "value" in nutrient:
            # Calories per serving is available
            if "unitName" in nutrient and nutrient["unitName"] == "kcal":
                calories_per_serving = nutrient["value"]
        
        # Check for calories per 100g
        if nutrient["nutrientName"] == "Energy" and "value" in nutrient:
            calories_per_100g = nutrient["value"]

    # If calories per serving is not available, use calories per 100g
    if calories_per_serving is None and calories_per_100g is not None:
        calories_per_serving = calories_per_100g  # Assume 100g portion size if per-serving data is missing

    # If no calories data is found
    if calories_per_serving is None:
        raise HTTPException(status_code=404, detail="Calories data not available for the dish")

    # Multiply by the number of servings
    total_calories = calories_per_serving * servings

    return total_calories

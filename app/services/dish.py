import requests
from fastapi import HTTPException
from app.config import Config

def fetch_dish_data(dish_name: str, servings: int):
    if servings <= 0:
        raise HTTPException(status_code=400, detail="Servings must be greater than 0")

    params = {
        'query': dish_name,
        'api_key': Config.API_KEY,
        'pageSize': 10  # More results for potential fuzzy matching (optional)
    }

    response = requests.get(Config.USDA_API_URL, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching data from USDA API")

    data = response.json()
    if "foods" not in data or not data["foods"]:
        raise HTTPException(status_code=404, detail="Dish not found")

    # Just use the first result (or apply fuzzy matching here later)
    food_item = data["foods"][0]

    # Initialize nutrient values
    calories = protein = fat = carbs = None

    for nutrient in food_item.get("foodNutrients", []):
        name = nutrient.get("nutrientName")
        value = nutrient.get("value")

        if name == "Energy" and nutrient.get("unitName", "").upper() == "KCAL":
            calories = value
        elif name == "Protein":
            protein = value
        elif name == "Total lipid (fat)":
            fat = value
        elif name == "Carbohydrate, by difference":
            carbs = value

    if calories is None:
        raise HTTPException(status_code=404, detail="Calories data not available for the dish")

    # Multiply by servings
    result = {
        "matched_dish_name": food_item["description"],
        "calories": round(calories * servings, 2) if calories is not None else None,
        "protein": round(protein * servings, 2) if protein is not None else None,
        "fat": round(fat * servings, 2) if fat is not None else None,
        "carbs": round(carbs * servings, 2) if carbs is not None else None,
        "serving_size": servings
    }

    return result

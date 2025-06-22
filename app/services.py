# # app/services.py

# import requests
# from fastapi import HTTPException
# from .config import Config

# # Helper function to fetch data from USDA API
# def fetch_dish_data(dish_name: str):
#     params = {
#         'query': dish_name,
#         'api_key': Config.API_KEY,
#         'pageSize': 1  # Get the most relevant result
#     }
#     response = requests.get(Config.USDA_API_URL, params=params)
#     if response.status_code != 200:
#         raise HTTPException(status_code=500, detail="Error fetching data from USDA API")
    
#     data = response.json()
#     if "foods" not in data or len(data["foods"]) == 0:
#         raise HTTPException(status_code=404, detail="Dish not found")
    
#     # Extract relevant information
#     food_item = data["foods"][0]
#     calories_per_100g = food_item["foodNutrients"][0]["value"]
#     calories_per_serving = calories_per_100g  # Assume per serving for simplicity

#     return calories_per_serving

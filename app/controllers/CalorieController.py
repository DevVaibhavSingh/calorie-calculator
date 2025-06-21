# app/controllers/CalorieController.py

from fastapi import APIRouter, Depends, HTTPException
from app.models.CalorieRequest import CalorieRequest
from app.models.CalorieResponse import CalorieResponse
from app.services.calorie_service import get_calorie_info
from app.services.cache_service import get_cache, set_cache
from app.dependencies.auth import get_current_user  # Import the dependency here
from app.models.user import User  # Add this import to bring in the User model
import asyncio

router = APIRouter()

@router.post("/get-calories", response_model=CalorieResponse)
async def get_calories(request: CalorieRequest, current_user: User = Depends(get_current_user)):
    """
    Get calorie information for a dish and its servings.
    Only accessible to logged-in users.
    """
    # Generate cache key based on dish_name and servings
    cache_key = f"calories:{request.dish_name}:{request.servings}"

    # Check if the response is cached
    cached_response = await asyncio.to_thread(get_cache, cache_key)

    if cached_response:
        # If cached response exists, return it with the cache flag set to true
        cached_response["cache"] = True
        return cached_response

    try:
        # If not cached, calculate the result
        response = await get_calorie_info(request)

        # Cache the result for future requests
        response_data = response.dict()  # Convert the response to a dictionary

        # Add cache flag to indicate it was not from cache
        response_data["cache"] = False

        # Set the cache
        await asyncio.to_thread(set_cache, cache_key, response_data)

        return response_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

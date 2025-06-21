# app/__init__.py

# This file marks the directory as a Python package.
# You can also add common imports to make it easier to use the app components.

from .config import Config
from .models import CalorieRequest, CalorieResponse
from .services.dish import fetch_dish_data
from .controllers.CalorieController import router
from app.services.calorie_service import get_calorie_info

# Optionally, you could initialize certain settings, etc.

# app/config.py

import os
from dotenv import load_dotenv
from pydantic import BaseSettings

# Load environment variables from .env file
load_dotenv()

class Config:
    API_KEY = os.getenv("USDA_API_KEY")
    USDA_API_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"


class Settings(BaseSettings):
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY', 'LWO9U6PgpmsHHVK0z8gY0-Dk2ZQf0_ya-gIJ6_y4wAs')
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///./test.db')  # Replace with actual DB URL

    class Config:
        env_file = ".env"

settings = Settings()


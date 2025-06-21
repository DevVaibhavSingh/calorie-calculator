# app/services/cache_service.py

import redis
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file (if using dotenv)
load_dotenv()

REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)

# Utility function to get cached data
def get_cache(key: str):
    client = redis.StrictRedis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        db=0
    )
    
    cached_data = client.get(key)
    
    if cached_data:
        # Add key to cached data for cache to tur
        return json.loads(cached_data)
    
    return None

# Utility function to set cache data
def set_cache(key: str, data: dict, ttl: int = 60):
    client = redis.StrictRedis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        db=0
    )
    
    # Set the cache with TTL (Time-to-Live)
    client.setex(key, ttl, json.dumps(data))

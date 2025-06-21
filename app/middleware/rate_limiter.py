# app/middleware/rate_limiter.py

import time
import redis
import asyncio
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app.config import Config  # Assuming the Redis connection URL and other config are in your Config file

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis_url: str, limit: int = 15, period: int = 60):
        """
        Initialize the RateLimitMiddleware with Redis.
        :param app: FastAPI app.
        :param redis_url: Redis connection URL (e.g., 'redis://localhost:6379').
        :param limit: Maximum number of requests allowed per period.
        :param period: Time period in seconds for rate-limiting.
        """
        super().__init__(app)
        self.redis_url = redis_url
        self.limit = limit
        self.period = period

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        client = redis.StrictRedis.from_url(self.redis_url)  # Create Redis client

        # Construct Redis key to track requests from the IP
        redis_key = f"rate_limit:{ip}"

        current_time = time.time()
        
        # Use asyncio.to_thread to run the synchronous Redis operations asynchronously
        request_count = await asyncio.to_thread(self.get_request_count, client, redis_key)
        
        # Clean up old request timestamps that are beyond the rate limit window
        await asyncio.to_thread(self.cleanup_old_requests, client, redis_key, current_time)
        
        # If the IP has exceeded the limit, reject the request
        if request_count >= self.limit:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded, try again later."}
            )

        # Add the current timestamp to the sorted set to track the request
        await asyncio.to_thread(self.add_request_timestamp, client, redis_key, current_time)
        
        # Set an expiration time for the key (in this case, the duration of the period)
        await asyncio.to_thread(self.set_key_expiry, client, redis_key)

        # Proceed with the request
        response = await call_next(request)
        return response

    def get_request_count(self, client: redis.StrictRedis, redis_key: str) -> int:
        """
        Get the current count of requests for the given key.
        """
        return client.zcard(redis_key)

    def cleanup_old_requests(self, client: redis.StrictRedis, redis_key: str, current_time: float):
        """
        Remove old request timestamps that are beyond the rate limit window.
        """
        client.zremrangebyscore(redis_key, 0, current_time - self.period)

    def add_request_timestamp(self, client: redis.StrictRedis, redis_key: str, current_time: float):
        """
        Add the current timestamp to the sorted set to track the request.
        """
        client.zadd(redis_key, {current_time: current_time})

    def set_key_expiry(self, client: redis.StrictRedis, redis_key: str):
        """
        Set the expiration time for the Redis key.
        """
        client.expire(redis_key, self.period)

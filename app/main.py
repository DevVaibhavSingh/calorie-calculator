# app/main.py

from fastapi import FastAPI
from app.controllers.CalorieController import router as calorie_router
from app.middleware.rate_limiter import RateLimitMiddleware
from app.controllers.AuthController import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.DishTrackerContoller import router as dish_tracker_router

origins = [
    "http://localhost:3000",  # frontend dev URL
    "https://yourdomain.com",  # production frontend
]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Or use ["*"] to allow all (not for prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routes from controllers
app.include_router(calorie_router)
app.include_router(dish_tracker_router)

# Add the rate limit middleware (with Redis connection URL)
app.add_middleware(RateLimitMiddleware, redis_url='redis://redis:6379', limit=15, period=60)
app.include_router(auth_router, prefix="/auth")

@app.get("/")

def read_root():
    return {"message": "Welcome to the Calorie API!"}

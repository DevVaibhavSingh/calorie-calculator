# app/main.py

from fastapi import FastAPI
from app.controllers.CalorieController import router as calorie_router
from app.middleware.rate_limiter import RateLimitMiddleware
from app.controllers.AuthController import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.DishTrackerContoller import router as dish_tracker_router
from fastapi.requests import Request

origins = [
    "http://localhost:3000",  # frontend dev URL
    "https://calorie-calculator-git-main-realvaibhavsingh-gmailcoms-projects.vercel.app/",  # production frontend
]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Or use ["*"] to allow all (not for prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_https_scheme(request: Request, call_next):
    if request.headers.get("x-forwarded-proto") == "https":
        request.scope["scheme"] = "https"
    response = await call_next(request)
    return response

@app.middleware("http")
async def force_https(request: Request, call_next):
    # Check if the request came through HTTP (via the X-Forwarded-Proto header)
    if request.headers.get("X-Forwarded-Proto") == "http":
        # If the request was HTTP, redirect to the HTTPS version
        url = request.url.replace(scheme="https")
        return RedirectResponse(url=str(url))
    
    # If the request was already HTTPS, proceed with the request
    response = await call_next(request)
    return response

# Include the routes from controllers
app.include_router(calorie_router)
app.include_router(dish_tracker_router)

# Add the rate limit middleware (with Redis connection URL)
app.add_middleware(RateLimitMiddleware, redis_url='redis://redis:6379', limit=15, period=60)
app.include_router(auth_router, prefix="/auth")

@app.get("/")

def read_root():
    return {"message": "Welcome to the Calorie API!"}

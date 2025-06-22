# app/controllers/DishTrackerController.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.models.TrackedDish import TrackedDish
from app.models.TrackDishRequest import TrackedDishRequest
from app.models.TrackDishResponse import TrackedDishResponse
from typing import List

router = APIRouter()

@router.post("/track-dish", response_model=TrackedDishResponse)
def track_dish(
    dish_data: TrackedDishRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tracked_dish = TrackedDish(
        user_id=current_user.id,
        dish_name=dish_data.dish_name,
        servings=dish_data.servings,
        calories_per_serving=dish_data.calories_per_serving,
        total_calories=dish_data.total_calories,
        source=dish_data.source,
        protein=dish_data.protein,
        carbs=dish_data.carbs,
        fat=dish_data.fat,
    )
    db.add(tracked_dish)
    db.commit()
    db.refresh(tracked_dish)
    return tracked_dish


@router.get("/my-dishes", response_model=List[TrackedDishResponse])
def get_tracked_dishes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(TrackedDish).filter(TrackedDish.user_id == current_user.id).order_by(TrackedDish.timestamp.desc()).all()

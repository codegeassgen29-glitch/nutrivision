# This file handles food image uploads.
# When a logged-in user uploads a photo of food, we:
# 1. Save the image file to disk
# 2. Create a "Meal" record in the database linking to that image + user
# 3. Return the created meal
#
# Later milestones will plug AI detection into this same flow.

import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from app.services.detection_service import detect_food
from app.models.detected_food import DetectedFood
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.meal import Meal
from app.schemas.meal import MealOut
from app.data.nutrition_table import get_nutrition
from datetime import date
from typing import Optional
from fastapi import Query
from sqlalchemy import func
from fastapi import Path
from app.schemas.detected_food import DetectedFoodUpdate
router = APIRouter(prefix="/meals", tags=["Meals"])

# Folder where uploaded images get saved.
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Only allow these image types, to avoid people uploading random files
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}


@router.post("/upload", response_model=MealOut, status_code=status.HTTP_201_CREATED)
def upload_meal_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Uploads a food image and creates a Meal record for the logged-in user.
    """

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {file.content_type}. Allowed: jpg, png, webp.",
        )

    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    new_meal = Meal(
        user_id=current_user.id,
        image_path=f"uploads/{unique_filename}",
    )

    db.add(new_meal)
    db.commit()
    db.refresh(new_meal)
    # ---------------------------------------------------------
    # Run AI food detection on the uploaded image
    # ---------------------------------------------------------
    # This calls our YOLOv8 model (see services/detection_service.py)
    # and gets back a list of detected foods with confidence scores.
    detected_items = detect_food(file_path)

    # Save each detected food as a row in the database, linked to this meal
    for item in detected_items:
        # Look up nutrition data for this food (may be None if unknown)
        nutrition = get_nutrition(item["food_name"])

        detected_food = DetectedFood(
            meal_id=new_meal.id,
            food_name=item["food_name"],
            confidence=item["confidence"],
            calories=nutrition["calories"] if nutrition else None,
            protein=nutrition["protein"] if nutrition else None,
            carbs=nutrition["carbs"] if nutrition else None,
            fat=nutrition["fat"] if nutrition else None,
        )
        db.add(detected_food)

    db.commit()
    db.refresh(new_meal)  # reload so new_meal.detected_foods includes the new rows

    return new_meal
@router.get("", response_model=list[MealOut])
def get_meal_history(
    start_date: Optional[date] = Query(None, description="Filter meals from this date onward"),
    end_date: Optional[date] = Query(None, description="Filter meals up to this date"),
    limit: int = Query(20, ge=1, le=100, description="Max number of meals to return"),
    offset: int = Query(0, ge=0, description="Number of meals to skip (for pagination)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns the logged-in user's meal history, newest first.
    Supports optional date filtering and pagination.
    """
    query = db.query(Meal).filter(Meal.user_id == current_user.id)

    # Apply date filters only if provided
    if start_date:
        query = query.filter(func.date(Meal.created_at) >= start_date)
    if end_date:
        query = query.filter(func.date(Meal.created_at) <= end_date)

    meals = (
        query
        .order_by(Meal.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return meals

@router.delete("/{meal_id}", status_code=status.HTTP_200_OK)
def delete_meal(
    meal_id: int = Path(..., description="ID of the meal to delete"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Deletes a meal (and its detected foods, via cascade) along with
    its uploaded image file. Only the meal's owner can delete it.
    """
    meal = db.query(Meal).filter(Meal.id == meal_id).first()

    if not meal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found")

    # Ownership check - critical security step
    if meal.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this meal")

    # Delete the image file from disk, if it exists
    full_image_path = os.path.join(os.path.dirname(__file__), "..", meal.image_path)
    if os.path.exists(full_image_path):
        os.remove(full_image_path)

    db.delete(meal)  # cascade="all, delete-orphan" on the model also removes detected_foods
    db.commit()

    return {"message": "Meal deleted successfully"}


@router.put("/{meal_id}/foods/{food_id}", response_model=MealOut)
def update_detected_food(
    meal_id: int,
    food_id: int,
    update_data: DetectedFoodUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Lets a user manually correct a detected food entry
    (e.g. fix a misclassification, or adjust nutrition values).
    """
    meal = db.query(Meal).filter(Meal.id == meal_id).first()

    if not meal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found")

    if meal.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to edit this meal")

    food = db.query(DetectedFood).filter(
        DetectedFood.id == food_id,
        DetectedFood.meal_id == meal_id,
    ).first()

    if not food:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Detected food not found for this meal")

    # Only update fields the client actually provided
    if update_data.food_name is not None:
        food.food_name = update_data.food_name
    if update_data.calories is not None:
        food.calories = update_data.calories
    if update_data.protein is not None:
        food.protein = update_data.protein
    if update_data.carbs is not None:
        food.carbs = update_data.carbs
    if update_data.fat is not None:
        food.fat = update_data.fat

    db.commit()
    db.refresh(meal)

    return meal
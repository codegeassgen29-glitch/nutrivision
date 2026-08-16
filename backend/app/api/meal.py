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
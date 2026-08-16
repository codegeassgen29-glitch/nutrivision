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

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.meal import Meal
from app.schemas.meal import MealOut

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

    return new_meal
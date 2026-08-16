from pydantic import BaseModel
from datetime import datetime
from app.schemas.detected_food import DetectedFoodOut

class MealOut(BaseModel):
    id: int
    image_path: str
    created_at: datetime
    detected_foods: list[DetectedFoodOut] = []

    class Config:
        from_attributes = True
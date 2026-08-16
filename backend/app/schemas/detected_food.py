from pydantic import BaseModel

class DetectedFoodOut(BaseModel):
    id: int
    food_name: str
    confidence: float
    calories: float | None
    protein: float | None
    carbs: float | None
    fat: float | None

    class Config:
        from_attributes = True
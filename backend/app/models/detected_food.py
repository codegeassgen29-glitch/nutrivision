from sqlalchemy import Column, Integer, String, Float, ForeignKey  # type: ignore[import]
from sqlalchemy.orm import relationship  # type: ignore[import]
from app.core.database import Base

class DetectedFood(Base):
    __tablename__ = "detected_foods"

    id = Column(Integer, primary_key=True, index=True)
    meal_id = Column(Integer, ForeignKey("meals.id"))
    food_name = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    calories = Column(Float, nullable=True)
    protein = Column(Float, nullable=True)
    carbs = Column(Float, nullable=True)
    fat = Column(Float, nullable=True)

    meal = relationship("Meal", back_populates="detected_foods")
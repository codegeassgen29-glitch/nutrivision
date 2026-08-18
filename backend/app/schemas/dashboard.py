# This schema defines the shape of data returned by the dashboard endpoint.
# It aggregates nutrition data across a user's meals into useful summaries.

from pydantic import BaseModel
from datetime import date
from app.schemas.meal import MealOut


class DailySummary(BaseModel):
    date: date
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fat: float


class DashboardSummary(BaseModel):
    today: DailySummary
    recent_meals: list[MealOut]
    weekly_calories: list[DailySummary]

    class DashboardSummary(BaseModel):
     today: DailySummary
    recent_meals: list[MealOut]
    weekly_calories: list[DailySummary]
    recommendations: list[str]
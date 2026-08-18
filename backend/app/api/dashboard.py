# This file provides dashboard/summary data - aggregated nutrition
# stats for the logged-in user, used to power the frontend dashboard.

from datetime import date, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.services.recommendation_service import generate_recommendations
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.meal import Meal
from app.models.detected_food import DetectedFood
from app.schemas.dashboard import DashboardSummary, DailySummary

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def get_daily_totals(db: Session, user_id: int, target_date: date) -> DailySummary:
    """
    Calculates total calories/protein/carbs/fat for all meals
    a user logged on a specific date.
    """
    # Join Meal -> DetectedFood, filter by user and date, sum nutrition columns
    result = (
        db.query(
            func.coalesce(func.sum(DetectedFood.calories), 0).label("calories"),
            func.coalesce(func.sum(DetectedFood.protein), 0).label("protein"),
            func.coalesce(func.sum(DetectedFood.carbs), 0).label("carbs"),
            func.coalesce(func.sum(DetectedFood.fat), 0).label("fat"),
        )
        .join(Meal, Meal.id == DetectedFood.meal_id)
        .filter(Meal.user_id == user_id)
        .filter(func.date(Meal.created_at) == target_date)
        .first()
    )

    return DailySummary(
        date=target_date,
        total_calories=round(result.calories, 1),
        total_protein=round(result.protein, 1),
        total_carbs=round(result.carbs, 1),
        total_fat=round(result.fat, 1),
    )


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns a full dashboard summary for the logged-in user:
    - Today's nutrition totals
    - Recent meals
    - Last 7 days of calorie totals (for charting)
    """
    today = date.today()

    # Today's totals
    today_summary = get_daily_totals(db, current_user.id, today)

    # Recent meals (last 10, newest first)
    recent_meals = (
        db.query(Meal)
        .filter(Meal.user_id == current_user.id)
        .order_by(Meal.created_at.desc())
        .limit(10)
        .all()
    )

    # Last 7 days of totals (for a weekly chart)
    weekly_calories = [
        get_daily_totals(db, current_user.id, today - timedelta(days=i))
        for i in range(6, -1, -1)  # 6 days ago -> today
    ]
    recommendations = generate_recommendations(
        total_calories=today_summary.total_calories,
        total_protein=today_summary.total_protein,
        total_carbs=today_summary.total_carbs,
        total_fat=today_summary.total_fat,
    )
    return DashboardSummary(
        today=today_summary,
        recent_meals=recent_meals,
        weekly_calories=weekly_calories,
        recommendations=recommendations,
    )
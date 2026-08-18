# This service generates simple, rule-based health recommendations
# based on a user's daily nutrition totals. It's NOT medical advice -
# just basic heuristics to nudge healthier eating habits, similar to
# what many fitness apps show.

def generate_recommendations(
    total_calories: float,
    total_protein: float,
    total_carbs: float,
    total_fat: float,
) -> list[str]:
    """
    Looks at today's nutrition totals and returns a list of
    plain-English tips. Rules are intentionally simple for now -
    can be made smarter later (e.g. personalized targets per user).
    """
    tips = []

    # Avoid division by zero if no meals logged yet
    if total_calories == 0:
        return ["No meals logged yet today. Log a meal to get personalized tips!"]

    # Rough general guidelines (not medical advice):
    # - Protein should be a meaningful share of calories for muscle maintenance
    # - Excessive carbs relative to protein can indicate an imbalanced diet
    # - High fat with low protein often signals processed/fried food patterns

    protein_calories = total_protein * 4  # 4 kcal per gram of protein
    carb_calories = total_carbs * 4        # 4 kcal per gram of carbs
    fat_calories = total_fat * 9            # 9 kcal per gram of fat

    protein_ratio = protein_calories / total_calories
    carb_ratio = carb_calories / total_calories
    fat_ratio = fat_calories / total_calories

    if protein_ratio < 0.15:
        tips.append("Your protein intake looks low today. Consider adding eggs, paneer, chicken, or dal.")

    if carb_ratio > 0.60:
        tips.append("This meal is high in carbohydrates. Balancing with more protein or vegetables could help.")

    if fat_ratio > 0.40:
        tips.append("Fat intake is relatively high today. Try to include leaner protein or grilled options.")

    if total_calories > 2500:
        tips.append("You've logged a high calorie intake today. Keep an eye on portion sizes if weight management is a goal.")

    if not tips:
        tips.append("Nice balance today! Your macros look reasonably well distributed.")

    return tips
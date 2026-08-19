# This file is our LOCAL nutrition database.
# Instead of calling an external API (which needs keys, network,
# rate limits), we keep a simple lookup table of common foods and
# their nutrition values PER SERVING (roughly 100g, unless noted).
#
# Format: food_name -> {calories, protein, carbs, fat} (all in grams
# except calories, which is in kcal)
#
# As we add custom-trained food classes later (biryani, dal, roti, etc.)
# we'll just add more entries here.

NUTRITION_TABLE = {
    "banana":    {"calories": 89,  "protein": 1.1, "carbs": 23.0, "fat": 0.3},
    "apple":     {"calories": 52,  "protein": 0.3, "carbs": 14.0, "fat": 0.2},
    "sandwich":  {"calories": 250, "protein": 12.0, "carbs": 30.0, "fat": 9.0},
    "orange":    {"calories": 47,  "protein": 0.9, "carbs": 12.0, "fat": 0.1},
    "broccoli":  {"calories": 34,  "protein": 2.8, "carbs": 7.0,  "fat": 0.4},
    "carrot":    {"calories": 41,  "protein": 0.9, "carbs": 10.0, "fat": 0.2},
    "pizza":     {"calories": 266, "protein": 11.0, "carbs": 33.0, "fat": 10.0},
    "donut":     {"calories": 452, "protein": 4.9, "carbs": 51.0, "fat": 25.0},
    "cake":      {"calories": 350, "protein": 5.0, "carbs": 50.0, "fat": 15.0},
    "hot dog":   {"calories": 290, "protein": 10.0, "carbs": 22.0, "fat": 18.0},

    # Custom-trained classes (Indian food, per typical serving)
    "chapati":      {"calories": 120, "protein": 3.0, "carbs": 18.0, "fat": 3.5},
    "dal makhni":   {"calories": 280, "protein": 9.0, "carbs": 26.0, "fat": 16.0},
    "fried rice":   {"calories": 333, "protein": 6.0, "carbs": 45.0, "fat": 14.0},
    "kadai paneer": {"calories": 320, "protein": 14.0, "carbs": 12.0, "fat": 24.0},
}



def get_nutrition(food_name: str) -> dict | None:
    """
    Looks up nutrition info for a given food name.
    Returns None if the food isn't in our table (unknown food).
    """
    return NUTRITION_TABLE.get(food_name.lower())
"""Recommendation filter presets."""

RECOMMEND_FILTERS = {
    "time_short": {"max_time": 60},
    "time_medium": {"max_time": 120},
    "cost_low": {"cost_level": "low"},
    "cost_high": {"cost_level": "high"},
    "meal_polo": {"category_slugs": ["polo"]},
    "meal_stew": {"category_slugs": ["stew", "traditional"]},
    "meal_kebab": {"category_slugs": ["kebab"]},
    "meal_ash": {"category_slugs": ["ash"]},
    "veg_only": {"vegetarian": True},
    "vegan_only": {"vegan": True},
    "available_now": {"available_now": True},
    "one_missing": {"one_missing": True},
}

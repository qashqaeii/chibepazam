from services.recommendation_service import RecommendationService
from services.random_service import RandomService
from database.repositories.recipes import RecipesRepository


class DecisionService:
    """Smart multi-step food decision flow."""

    def __init__(self):
        self.recs = RecommendationService()
        self.random = RandomService()
        self.repo = RecipesRepository()

    def resolve(self, filters: dict, user_id: int, limit: int = 5) -> list[dict]:
        rec_filters = {
            "max_time": filters.get("max_time"),
            "cost_level": filters.get("cost_level"),
            "category_slugs": filters.get("category_slugs"),
            "protein": filters.get("protein"),
            "vegetarian": filters.get("vegetarian"),
            "vegan": filters.get("vegan"),
            "available_now": filters.get("available_now", False),
            "one_missing": filters.get("one_missing", False),
        }
        items, _, _ = self.recs.get_recommendations(
            user_id, page=1, per_page=limit, filters=rec_filters
        )
        if items:
            return [x["recipe"] for x in items]
        recipe = self.random.get_random("full", user_id=user_id, exclude_disliked=True)
        return [recipe] if recipe else []

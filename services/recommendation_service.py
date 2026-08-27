from database.repositories.recipes import RecipesRepository
from database.repositories.pantry import PantryRepository
from database.repositories.settings import SettingsRepository
from services.recipe_service import RecipeService

ANIMAL_INGREDIENT_SLUGS = {
    "chicken",
    "red-meat",
    "ground-meat",
    "fish",
    "tuna",
    "shank",
    "egg",
    "yogurt",
    "kashk",
    "butter",
    "strained-yogurt",
}


class RecommendationService:
    def __init__(self):
        self.recipes_repo = RecipesRepository()
        self.pantry_repo = PantryRepository()
        self.settings_repo = SettingsRepository()
        self.recipe_service = RecipeService()

    def get_recommendations(
        self, user_id: int, page: int = 1, per_page: int = 5
    ) -> tuple[list, int, int]:
        user_ingredients = self.pantry_repo.get_combined_ids(user_id)
        if not user_ingredients:
            return [], 1, 1

        settings = self.settings_repo.get(user_id)
        forbidden = self.settings_repo.get_forbidden_ids(user_id)

        recipes = self.recipes_repo.get_all_active()
        scored = []
        seen_ids: set[int] = set()

        for recipe in recipes:
            if recipe["id"] in seen_ids:
                continue
            seen_ids.add(recipe["id"])
            if settings and settings.get("diet_type") == "vegetarian" and not recipe.get("is_vegetarian"):
                continue

            ingredients = self.recipes_repo.get_ingredients(recipe["id"])
            if settings and settings.get("diet_type") == "vegan":
                if any(
                    ri.get("slug") in ANIMAL_INGREDIENT_SLUGS and not ri.get("is_optional")
                    for ri in ingredients
                ):
                    continue
            if any(ri["ingredient_id"] in forbidden for ri in ingredients):
                continue

            match = self.recipe_service._calculate_match(ingredients, user_ingredients)
            if match.score > 0:
                scored.append({
                    "recipe": recipe,
                    "score": match.score,
                    "have_count": match.have_count,
                    "missing_count": match.missing_count,
                })

        scored.sort(key=lambda x: (-x["score"], x["missing_count"]))

        from utils.pagination import paginate
        page_items, current_page, total_pages = paginate(scored, page, per_page)
        return page_items, current_page, total_pages

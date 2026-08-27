from database.repositories.recipes import RecipesRepository
from database.repositories.pantry import PantryRepository
from database.repositories.settings import SettingsRepository
from database.repositories.dislikes import DislikesRepository
from services.recipe_service import RecipeService

ANIMAL_INGREDIENT_SLUGS = {
    "chicken", "red-meat", "ground-meat", "ground-chicken", "fish", "tuna",
    "shank", "shrimp", "liver", "sausage", "mortadella", "egg", "yogurt",
    "kashk", "butter", "strained-yogurt", "milk", "cheese", "cream",
    "pizza-cheese", "ghee", "honey", "doogh",
}


class RecommendationService:
    def __init__(self):
        self.recipes_repo = RecipesRepository()
        self.pantry_repo = PantryRepository()
        self.settings_repo = SettingsRepository()
        self.dislikes_repo = DislikesRepository()
        self.recipe_service = RecipeService()

    def get_recommendations(
        self,
        user_id: int,
        page: int = 1,
        per_page: int = 5,
        filters: dict | None = None,
    ) -> tuple[list, int, int]:
        filters = filters or {}
        user_ingredients = self.pantry_repo.get_combined_ids(user_id)
        if filters.get("available_now") and not user_ingredients:
            return [], 1, 1
        if not user_ingredients and not filters.get("available_now"):
            return [], 1, 1

        settings = self.settings_repo.get(user_id)
        forbidden = self.settings_repo.get_forbidden_ids(user_id)
        disliked = self.dislikes_repo.get_ids(user_id)

        recipes = self.recipes_repo.get_all_active()
        scored = []

        for recipe in recipes:
            if recipe["id"] in disliked:
                continue
            if not self._passes_filters(recipe, settings, filters):
                continue

            ingredients = self.recipes_repo.get_ingredients(recipe["id"])
            ingredients = self.recipe_service._scale_recipe_ingredients(recipe, ingredients, user_id)

            if settings and settings.get("diet_type") == "vegetarian" and not recipe.get("is_vegetarian"):
                continue
            if settings and settings.get("diet_type") == "vegan":
                if any(
                    ri.get("slug") in ANIMAL_INGREDIENT_SLUGS and not ri.get("is_optional")
                    for ri in ingredients
                ):
                    continue
            if filters.get("vegetarian") and not recipe.get("is_vegetarian"):
                continue
            if filters.get("vegan"):
                if any(
                    ri.get("slug") in ANIMAL_INGREDIENT_SLUGS and not ri.get("is_optional")
                    for ri in ingredients
                ):
                    continue
            if any(ri["ingredient_id"] in forbidden for ri in ingredients):
                continue

            match = self.recipe_service._calculate_match(ingredients, user_ingredients)
            if match.score <= 0:
                continue
            if filters.get("one_missing") and match.missing_count != 1:
                continue
            if filters.get("available_now") and match.missing_count > 0:
                continue

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

    def _passes_filters(self, recipe: dict, settings: dict | None, filters: dict) -> bool:
        if filters.get("max_time"):
            total = recipe.get("prep_time", 0) + recipe.get("cook_time", 0)
            if total > filters["max_time"]:
                return False
        if filters.get("cost_level") and recipe.get("cost_level") != filters["cost_level"]:
            return False
        if filters.get("category_slugs"):
            slug = recipe.get("category_slug")
            if not slug:
                return False
            if slug not in filters["category_slugs"]:
                return False
        if filters.get("protein"):
            slugs = {"chicken": ["chicken", "ground-chicken"], "meat": ["red-meat", "ground-meat", "shank"], "fish": ["fish", "tuna", "shrimp"]}
            need = slugs.get(filters["protein"], [])
            ings = self.recipes_repo.get_ingredients(recipe["id"])
            if not any(i.get("slug") in need for i in ings):
                return False
        return True

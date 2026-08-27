from dataclasses import dataclass

from database.repositories.recipes import RecipesRepository
from database.repositories.favorites import FavoritesRepository
from database.repositories.history import HistoryRepository
from database.repositories.pantry import PantryRepository
from database.repositories.settings import SettingsRepository
from database.repositories.ratings import RatingsRepository
from database.repositories.dislikes import DislikesRepository
from services.rating_service import RatingService
from services.dislike_service import DislikeService
from utils.servings import scale_ingredients


@dataclass
class RecipeMatch:
    recipe: dict
    score: float
    have_count: int
    missing_count: int
    missing_ingredients: list[dict]
    have_ingredients: list[dict]


class RecipeService:
    def __init__(self):
        self.repo = RecipesRepository()
        self.favorites_repo = FavoritesRepository()
        self.history_repo = HistoryRepository()
        self.pantry_repo = PantryRepository()
        self.settings_repo = SettingsRepository()
        self.ratings_repo = RatingsRepository()
        self.dislikes_repo = DislikesRepository()
        self.rating_service = RatingService()
        self.dislike_service = DislikeService()

    def _user_servings(self, user_id: int) -> int:
        settings = self.settings_repo.get(user_id)
        return int((settings or {}).get("servings") or 4)

    def _scale_recipe_ingredients(self, recipe: dict, ingredients: list[dict], user_id: int) -> list[dict]:
        target = self._user_servings(user_id)
        base = recipe.get("servings") or 4
        return scale_ingredients(ingredients, base, target)

    def get_recipe(self, recipe_id: int) -> dict | None:
        return self.repo.get_by_id(recipe_id)

    def get_recipe_detail(self, recipe_id: int, user_id: int) -> dict | None:
        recipe = self.repo.get_by_id(recipe_id)
        if not recipe:
            return None
        ingredients = self.repo.get_ingredients(recipe_id)
        ingredients = self._scale_recipe_ingredients(recipe, ingredients, user_id)
        user_ingredients = self.pantry_repo.get_combined_ids(user_id)
        match = self._calculate_match(ingredients, user_ingredients)
        recipe = dict(recipe)
        recipe["ingredients"] = ingredients
        recipe["match"] = match
        recipe["is_favorite"] = self.favorites_repo.is_favorite(user_id, recipe_id)
        recipe["user_rating"] = self.ratings_repo.get_user_rating(user_id, recipe_id)
        recipe["is_disliked"] = self.dislikes_repo.is_disliked(user_id, recipe_id)
        recipe["display_servings"] = self._user_servings(user_id)
        avg, count = self.ratings_repo.get_aggregate(recipe_id)
        recipe["rating"] = avg
        recipe["rating_count"] = count
        return recipe

    def view_recipe(self, user_id: int, recipe_id: int) -> dict | None:
        recipe = self.get_recipe_detail(recipe_id, user_id)
        if recipe:
            self.history_repo.add(user_id, recipe_id)
        return recipe

    def toggle_favorite(self, user_id: int, recipe_id: int) -> bool:
        if self.favorites_repo.is_favorite(user_id, recipe_id):
            self.favorites_repo.remove(user_id, recipe_id)
            return False
        self.favorites_repo.add(user_id, recipe_id)
        return True

    def get_similar(self, recipe_id: int) -> list[dict]:
        return self.repo.get_similar(recipe_id)

    def _calculate_match(
        self, recipe_ingredients: list[dict], user_ingredient_ids: set[int]
    ) -> RecipeMatch:
        if not recipe_ingredients:
            return RecipeMatch({}, 0, 0, 0, [], [])

        total_weight = 0
        earned_weight = 0
        have = []
        missing = []

        for ri in recipe_ingredients:
            importance = ri.get("importance", 5)
            if ri.get("is_common") or importance <= 1:
                weight = 1
            else:
                weight = importance

            total_weight += weight
            if ri["ingredient_id"] in user_ingredient_ids:
                earned_weight += weight
                have.append(ri)
            else:
                if importance >= 5 or ri.get("is_required"):
                    missing.append(ri)

        score = round((earned_weight / total_weight) * 100, 1) if total_weight else 0
        score = max(0.0, min(100.0, score))
        return RecipeMatch(
            recipe={},
            score=score,
            have_count=len(have),
            missing_count=len(missing),
            missing_ingredients=missing,
            have_ingredients=have,
        )

    def format_cook_time(self, recipe: dict) -> int:
        return recipe.get("prep_time", 0) + recipe.get("cook_time", 0)

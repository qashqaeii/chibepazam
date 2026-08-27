from database.repositories.recipes import RecipesRepository
from database.repositories.ingredients import IngredientsRepository
from database.repositories.recipe_categories import RecipeCategoriesRepository
from database.repositories.substitutes import SubstitutesRepository
from services.analytics_service import AnalyticsService
from services.broadcast_service import BroadcastService


class AdminService:
    def __init__(self):
        self.recipes = RecipesRepository()
        self.ingredients = IngredientsRepository()
        self.categories = RecipeCategoriesRepository()
        self.substitutes = SubstitutesRepository()
        self.analytics = AnalyticsService()
        self.broadcast = BroadcastService()

    def toggle_recipe(self, recipe_id: int) -> bool:
        return self.recipes.toggle_active(recipe_id)

    def toggle_ingredient(self, ingredient_id: int) -> bool:
        return self.ingredients.toggle_active(ingredient_id)

    def toggle_category(self, category_id: int) -> bool:
        return self.categories.toggle_active(category_id)

    def deactivate_substitute(self, sub_id: int) -> None:
        self.substitutes.deactivate(sub_id)

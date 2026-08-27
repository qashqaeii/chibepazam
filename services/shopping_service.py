from database.repositories.shopping_cart import ShoppingCartRepository
from database.repositories.recipes import RecipesRepository
from database.repositories.pantry import PantryRepository
from database.repositories.settings import SettingsRepository
from services.recipe_service import RecipeService
from utils.servings import scale_ingredient_row
from utils.shopping import build_merged_shopping_list


class ShoppingService:
    def __init__(self):
        self.cart = ShoppingCartRepository()
        self.recipes = RecipesRepository()
        self.recipe_service = RecipeService()

    def add_recipe(self, user_id: int, recipe_id: int) -> int:
        self.cart.add(user_id, recipe_id)
        return self.cart.count(user_id)

    def remove_recipe(self, user_id: int, recipe_id: int) -> int:
        self.cart.remove(user_id, recipe_id)
        return self.cart.count(user_id)

    def clear(self, user_id: int) -> None:
        self.cart.clear(user_id)

    def count(self, user_id: int) -> int:
        return self.cart.count(user_id)

    def build_merged_list(self, user_id: int) -> tuple[str, list[dict]]:
        recipe_ids = self.cart.get_recipe_ids(user_id)
        settings = SettingsRepository().get(user_id) or {"servings": 4}
        target = int(settings.get("servings") or 4)
        pantry = PantryRepository().get_combined_ids(user_id)
        merged: dict[int, dict] = {}
        names: list[str] = []

        for rid in recipe_ids:
            recipe = self.recipes.get_by_id(rid)
            if not recipe:
                continue
            names.append(recipe["name"])
            ingredients = self.recipes.get_ingredients(rid)
            scaled = [
                scale_ingredient_row(ri, recipe.get("servings") or 4, target)
                for ri in ingredients
            ]
            match = self.recipe_service._calculate_match(scaled, pantry)
            for item in match.missing_ingredients:
                iid = item["ingredient_id"]
                if iid not in merged:
                    merged[iid] = dict(item)
                else:
                    merged[iid] = self._merge_qty(merged[iid], item)

        items = list(merged.values())
        text = build_merged_shopping_list(names, items, target)
        return text, items

    def _merge_qty(self, a: dict, b: dict) -> dict:
        from utils.shopping import merge_amounts

        out = dict(a)
        out["amount"] = merge_amounts(a.get("amount"), b.get("amount"))
        return out

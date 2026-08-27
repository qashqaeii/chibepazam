from database.repositories.ingredients import IngredientsRepository
from database.repositories.pantry import PantryRepository


class IngredientService:
    def __init__(self):
        self.ingredients_repo = IngredientsRepository()
        self.pantry_repo = PantryRepository()

    def get_categories(self) -> list[dict]:
        return self.ingredients_repo.get_categories()

    def get_category(self, category_id: int) -> dict | None:
        return self.ingredients_repo.get_category(category_id)

    def get_by_category(self, category_id: int) -> list[dict]:
        return self.ingredients_repo.get_by_category(category_id)

    def toggle_pantry(self, user_id: int, ingredient_id: int) -> bool:
        return self.pantry_repo.toggle(user_id, ingredient_id)

    def get_selected_ids(self, user_id: int) -> set[int]:
        return self.pantry_repo.get_user_ingredient_ids(user_id)

    def get_combined_ids(self, user_id: int) -> set[int]:
        return self.pantry_repo.get_combined_ids(user_id)

    def get_selected_ingredients(self, user_id: int) -> list[dict]:
        ids = list(self.pantry_repo.get_user_ingredient_ids(user_id))
        return self.ingredients_repo.get_by_ids(ids)

    def clear_pantry(self, user_id: int) -> None:
        self.pantry_repo.clear(user_id)

    def pantry_count(self, user_id: int) -> int:
        return self.pantry_repo.count(user_id)

    def toggle_permanent(self, user_id: int, ingredient_id: int) -> bool:
        return self.pantry_repo.toggle_permanent(user_id, ingredient_id)

    def get_permanent_ids(self, user_id: int) -> set[int]:
        return self.pantry_repo.get_permanent_ids(user_id)

    def get_all_active(self) -> list[dict]:
        return self.ingredients_repo.get_all_active()

    def get_common_for_permanent(self) -> list[dict]:
        return self.ingredients_repo.get_common_ingredients()

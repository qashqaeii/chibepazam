from database.repositories.cooked import CookedRepository


class CookedService:
    def __init__(self):
        self.repo = CookedRepository()

    def mark_cooked(self, user_id: int, recipe_id: int) -> int:
        return self.repo.mark_cooked(user_id, recipe_id)

    def stats_for_user(self, user_id: int) -> dict:
        return {
            "total_cooks": self.repo.count_for_user(user_id),
            "distinct_recipes": self.repo.distinct_count(user_id),
        }

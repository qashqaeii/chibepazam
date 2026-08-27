from database.repositories.dislikes import DislikesRepository


class DislikeService:
    def __init__(self):
        self.repo = DislikesRepository()

    def get_disliked_ids(self, user_id: int) -> set[int]:
        return self.repo.get_ids(user_id)

    def toggle(self, user_id: int, recipe_id: int) -> bool:
        return self.repo.toggle(user_id, recipe_id)

    def is_disliked(self, user_id: int, recipe_id: int) -> bool:
        return self.repo.is_disliked(user_id, recipe_id)

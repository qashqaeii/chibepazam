from database.repositories.ratings import RatingsRepository

RATING_LABELS = {
    "love": "😍 عالی",
    "good": "🙂 خوب",
    "ok": "😐 معمولی",
    "bad": "👎 دوست نداشتم",
}


class RatingService:
    def __init__(self):
        self.repo = RatingsRepository()

    def set_rating(self, user_id: int, recipe_id: int, rating: str) -> None:
        if rating not in RATING_LABELS:
            raise ValueError("invalid rating")
        self.repo.set_rating(user_id, recipe_id, rating)

    def get_user_rating(self, user_id: int, recipe_id: int) -> str | None:
        return self.repo.get_user_rating(user_id, recipe_id)

    def get_display(self, recipe_id: int) -> str:
        avg, count = self.repo.get_aggregate(recipe_id)
        if count == 0:
            return f"⭐ {avg:.1f}  ·  بدون رأی کاربر"
        return f"⭐ {avg:.1f}  ·  {count} رأی"

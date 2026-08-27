from database.repositories.recipes import RecipesRepository
from database.repositories.events import EventsRepository
from database.repositories.dislikes import DislikesRepository


class RandomService:
    FILTERS = {
        "full": {},
        "fast": {"max_total_time": 60},
        "cheap": {"cost_level": "low"},
        "chicken": {"require_any_slugs": ["chicken", "ground-chicken"]},
        "meat": {"require_any_slugs": ["red-meat", "ground-meat", "shank"]},
        "vegetarian": {"is_vegetarian": True},
        "rice": {"require_any_slugs": ["rice"]},
        "bread": {"require_any_slugs": ["bread"]},
        "traditional": {"require_category_slugs": ["traditional", "stew", "ash"]},
    }

    def __init__(self):
        self.repo = RecipesRepository()
        self.events_repo = EventsRepository()
        self.dislikes_repo = DislikesRepository()

    def get_random(
        self,
        filter_key: str = "full",
        exclude_ids: list[int] | None = None,
        user_id: int | None = None,
        exclude_disliked: bool = True,
    ) -> dict | None:
        filters = self.FILTERS.get(filter_key, {})
        exclude = list(exclude_ids or [])
        if exclude_disliked and user_id:
            exclude.extend(self.dislikes_repo.get_ids(user_id))
        exclude = list(set(exclude)) if exclude else None
        return self.repo.get_random(
            difficulty=filters.get("difficulty"),
            cost_level=filters.get("cost_level"),
            is_vegetarian=filters.get("is_vegetarian"),
            exclude_ids=exclude,
            max_total_time=filters.get("max_total_time"),
            require_any_slugs=filters.get("require_any_slugs"),
            require_category_slugs=filters.get("require_category_slugs"),
        )

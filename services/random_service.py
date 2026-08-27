from database.repositories.recipes import RecipesRepository
from database.repositories.events import EventsRepository


class RandomService:
    FILTERS = {
        "full": {},
        "fast": {"difficulty": "easy"},
        "cheap": {"cost_level": "low"},
        "chicken": {"tag": "chicken"},
        "meat": {"tag": "meat"},
        "vegetarian": {"is_vegetarian": True},
        "rice": {"tag": "rice"},
        "bread": {"tag": "bread"},
        "traditional": {"tag": "traditional"},
    }

    def __init__(self):
        self.repo = RecipesRepository()
        self.events_repo = EventsRepository()

    def get_random(self, filter_key: str = "full", exclude_ids: list[int] | None = None) -> dict | None:
        filters = self.FILTERS.get(filter_key, {})
        difficulty = filters.get("difficulty")
        cost_level = filters.get("cost_level")
        is_vegetarian = filters.get("is_vegetarian")

        recipe = self.repo.get_random(
            difficulty=difficulty,
            cost_level=cost_level,
            is_vegetarian=is_vegetarian,
            exclude_ids=exclude_ids,
        )

        if recipe and filters.get("tag"):
            tag = filters["tag"]
            ingredients = self.repo.get_ingredients(recipe["id"])
            slugs = {ri.get("slug", "") for ri in ingredients}
            names = " ".join(ri.get("name", "") for ri in ingredients).lower()
            recipe_name = recipe.get("name", "").lower()

            tag_checks = {
                "chicken": lambda: any("مرغ" in n or "chicken" in s for n, s in zip(names, slugs)),
                "meat": lambda: any("گوشت" in n or "meat" in s for n, s in zip(names, slugs)),
                "rice": lambda: any("برنج" in n or "rice" in s for n, s in zip(names, slugs)),
                "bread": lambda: "نون" in recipe_name or "نان" in recipe_name,
                "traditional": lambda: True,
            }
            check = tag_checks.get(tag, lambda: True)
            if not check():
                return self.get_random(filter_key, (exclude_ids or []) + [recipe["id"]])

        return recipe

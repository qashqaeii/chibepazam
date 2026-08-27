from database.repositories.events import EventsRepository
from database.repositories.users import UsersRepository
from database.repositories.recipes import RecipesRepository
from database.repositories.favorites import FavoritesRepository
from database.repositories.cooked import CookedRepository


class AnalyticsService:
    def __init__(self):
        self.events = EventsRepository()
        self.users = UsersRepository()
        self.recipes = RecipesRepository()
        self.favorites = FavoritesRepository()
        self.cooked = CookedRepository()

    def dashboard(self) -> dict:
        return {
            "total_users": self.users.count_all(),
            "dau": self.users.count_active_today(),
            "searches_today": self.events.count_searches_today(),
            "random_today": self.events.count_today("random"),
            "favorites_total": self.users.count_favorites_total(),
            "cooked_total": self.cooked.count_all(),
            "top_recipes": self.favorites.count_popular(5) or [],
            "top_ingredients": self.users.top_pantry_ingredients(5),
            "top_searches": self.events.top_searches(5),
        }

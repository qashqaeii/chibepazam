from database.repositories.recipes import RecipesRepository
from database.repositories.events import EventsRepository


class SearchService:
    def __init__(self):
        self.repo = RecipesRepository()
        self.events_repo = EventsRepository()

    def search(self, user_id: int, query: str, limit: int = 10) -> list[dict]:
        query = query.strip()
        if len(query) < 2:
            return []
        results = self.repo.search(query, limit)
        self.events_repo.log_search(user_id, query)
        self.events_repo.log("search", user_id, {"query": query})
        return results

"""Navigation stack — Back returns to logical previous screen."""

from database.repositories.users import UsersRepository

# Current screen per user (in-memory, keyed by internal user_id)
_current: dict[int, dict] = {}


class NavService:
    SCREENS = (
        "home",
        "pantry_main",
        "pantry_category",
        "pantry_selected",
        "recommendations",
        "recipe_detail",
        "favorites",
        "history",
        "random_menu",
        "random_result",
        "search_prompt",
        "search_results",
        "settings",
        "settings_permanent",
        "settings_servings",
        "settings_diet",
        "profile",
        "admin_main",
        "admin_page",
    )

    def __init__(self):
        self._repo = UsersRepository()

    def get_current(self, user_id: int) -> dict | None:
        return _current.get(user_id)

    def set_current(self, user_id: int, screen: str, payload: dict | None = None) -> None:
        _current[user_id] = {"screen": screen, "payload": payload or {}}

    def push_current(self, user_id: int) -> None:
        cur = _current.get(user_id)
        if cur:
            self._repo.push_nav(user_id, cur["screen"], cur["payload"])

    def navigate(self, user_id: int, screen: str, payload: dict | None = None) -> None:
        """Push current screen then set new current (call before rendering forward)."""
        self.push_current(user_id)
        self.set_current(user_id, screen, payload)

    def replace(self, user_id: int, screen: str, payload: dict | None = None) -> None:
        """Update current screen without pushing (pagination, toggle)."""
        self.set_current(user_id, screen, payload)

    def clear(self, user_id: int) -> None:
        _current.pop(user_id, None)
        self._repo.clear_nav(user_id)

    def pop_and_get(self, user_id: int) -> dict | None:
        """Pop stack entry to navigate back to."""
        entry = self._repo.pop_nav(user_id)
        if entry:
            self.set_current(user_id, entry["screen"], entry.get("payload") or {})
            return entry
        return None


nav_service = NavService()

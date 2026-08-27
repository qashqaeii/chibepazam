"""Navigation stack — Back returns to logical previous screen."""

from database.repositories.users import UsersRepository
from database.repositories.screen_state import ScreenStateRepository

_current: dict[int, dict] = {}


class NavService:
    SCREENS = (
        "home",
        "pantry_main",
        "pantry_category",
        "pantry_selected",
        "recommendations",
        "recommend_filters",
        "recipe_detail",
        "recipe_similar",
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
        "settings_forbidden",
        "profile",
        "decision_flow",
        "shopping_cart",
        "admin_main",
        "admin_page",
    )

    def __init__(self):
        self._repo = UsersRepository()
        self._screen_repo = ScreenStateRepository()

    def _hydrate(self, user_id: int) -> dict | None:
        if user_id in _current:
            return _current[user_id]
        try:
            saved = self._screen_repo.load(user_id)
            if saved:
                _current[user_id] = saved
                return saved
        except Exception:
            pass
        return None

    def get_current(self, user_id: int) -> dict | None:
        return self._hydrate(user_id)

    def set_current(self, user_id: int, screen: str, payload: dict | None = None) -> None:
        entry = {"screen": screen, "payload": payload or {}}
        _current[user_id] = entry
        try:
            self._screen_repo.save(user_id, screen, payload or {})
        except Exception:
            pass

    def push_current(self, user_id: int) -> None:
        cur = self._hydrate(user_id)
        if cur:
            try:
                self._repo.push_nav(user_id, cur["screen"], cur["payload"])
            except Exception:
                pass

    def navigate(self, user_id: int, screen: str, payload: dict | None = None) -> None:
        self.push_current(user_id)
        self.set_current(user_id, screen, payload)

    def replace(self, user_id: int, screen: str, payload: dict | None = None) -> None:
        self.set_current(user_id, screen, payload)

    def clear(self, user_id: int) -> None:
        _current.pop(user_id, None)
        try:
            self._repo.clear_nav(user_id)
            self._screen_repo.clear(user_id)
        except Exception:
            pass

    def pop_and_get(self, user_id: int) -> dict | None:
        try:
            entry = self._repo.pop_nav(user_id)
        except Exception:
            entry = None
        if entry:
            self.set_current(user_id, entry["screen"], entry.get("payload") or {})
            return entry
        return None


nav_service = NavService()

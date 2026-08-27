"""In-memory user state manager for temporary states."""

from enum import Enum
from dataclasses import dataclass, field
from typing import Any


class UserState(str, Enum):
    NONE = "none"
    WAITING_SEARCH = "waiting_search"
    WAITING_ADMIN_BROADCAST = "waiting_admin_broadcast"
    WAITING_ADMIN_BROADCAST_PHOTO = "waiting_admin_broadcast_photo"
    WAITING_ADMIN_BROADCAST_BUTTON = "waiting_admin_broadcast_button"
    CONFIRM_ADMIN_BROADCAST = "confirm_admin_broadcast"
    WAITING_ADMIN_RECIPE_NAME = "waiting_admin_recipe_name"
    WAITING_ADMIN_INGREDIENT_NAME = "waiting_admin_ingredient_name"
    CONFIRM_PANTRY_CLEAR = "confirm_pantry_clear"


@dataclass
class StateData:
    state: UserState = UserState.NONE
    data: dict[str, Any] = field(default_factory=dict)


class UserStateManager:
    def __init__(self):
        self._states: dict[int, StateData] = {}

    def get(self, telegram_id: int) -> StateData:
        if telegram_id not in self._states:
            self._states[telegram_id] = StateData()
        return self._states[telegram_id]

    def set_state(self, telegram_id: int, state: UserState, **data: Any) -> None:
        self._states[telegram_id] = StateData(state=state, data=data)

    def clear(self, telegram_id: int) -> None:
        self._states.pop(telegram_id, None)

    def is_waiting(self, telegram_id: int, state: UserState) -> bool:
        return self.get(telegram_id).state == state


state_manager = UserStateManager()

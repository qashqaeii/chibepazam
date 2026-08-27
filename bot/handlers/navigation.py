"""Central screen renderer for Back/Home navigation."""

from telebot import TeleBot

from bot.handlers.base import safe_edit, show_main_menu
from services.nav_service import nav_service
from services.user_service import UserService
from utils.logger import setup_logger

logger = setup_logger(__name__)
user_service = UserService()


def render_screen(
    bot: TeleBot,
    chat_id: int,
    message_id: int,
    user_id: int,
    screen: str,
    payload: dict,
    telegram_id: int | None = None,
) -> bool:
    """Render a screen by name. Returns True if rendered."""
    from bot.handlers.pantry import (
        show_pantry_main,
        show_pantry_category,
        show_pantry_selected,
        show_recommendations,
    )
    from bot.handlers.recipe_handler import show_recipe
    from bot.handlers.favorites import show_favorites
    from bot.handlers.history import show_history
    from bot.handlers.random_food import show_random_menu, show_random_result
    from bot.handlers.search import show_search_results, show_search_prompt
    from bot.handlers.settings import show_settings, show_permanent, show_servings, show_diet
    from bot.handlers.profile import show_profile
    from bot.handlers.admin import show_admin_dashboard
    from bot.handlers.forbidden_settings import show_forbidden
    from bot.handlers.decision import show_decision_start
    from bot.handlers.shopping import show_cart
    from bot.handlers.pantry import show_recommend_filters

    tid = telegram_id

    try:
        if screen == "home":
            show_main_menu(bot, chat_id, message_id)
            nav_service.set_current(user_id, "home", {})
            return True

        if screen == "pantry_main":
            show_pantry_main(bot, chat_id, message_id, user_id)
            return True

        if screen == "pantry_category":
            show_pantry_category(
                bot, chat_id, message_id, user_id,
                payload.get("category_id", 1),
                payload.get("page", 1),
            )
            return True

        if screen == "pantry_selected":
            show_pantry_selected(bot, chat_id, message_id, user_id)
            return True

        if screen == "recommendations":
            show_recommendations(bot, chat_id, message_id, user_id, payload.get("page", 1))
            return True

        if screen == "recommend_filters":
            show_recommend_filters(bot, chat_id, message_id, user_id)
            return True

        if screen == "settings_forbidden":
            show_forbidden(bot, chat_id, message_id, user_id, payload.get("page", 1))
            return True

        if screen == "decision_flow":
            show_decision_start(bot, chat_id, message_id, user_id)
            return True

        if screen == "shopping_cart":
            show_cart(bot, chat_id, message_id, user_id)
            return True

        if screen == "recipe_similar":
            recipe_id = payload.get("recipe_id")
            if recipe_id:
                from services.recipe_service import RecipeService
                from bot.keyboards.recipe import recipe_list_keyboard, recipe_sub_keyboard
                from utils.screen import build_screen, ACTION_FOOTER
                similar = RecipeService().get_similar(recipe_id)
                if similar:
                    text = build_screen(
                        emoji="🔄", title="غذاهای مشابه",
                        description="این غذاها به غذای انتخابی شما نزدیک‌ترن:",
                        details=[f"📋  {len(similar)} پیشنهاد"], footer=ACTION_FOOTER,
                    )
                    safe_edit(bot, chat_id, message_id, text, recipe_list_keyboard(similar))
                    return True
                show_recipe(bot, chat_id, message_id, user_id, recipe_id)
                return True

        if screen == "recipe_detail":
            recipe_id = payload.get("recipe_id")
            if recipe_id:
                show_recipe(bot, chat_id, message_id, user_id, recipe_id)
                return True

        if screen == "favorites":
            show_favorites(bot, chat_id, message_id, user_id, payload.get("page", 1))
            return True

        if screen == "history":
            show_history(bot, chat_id, message_id, user_id)
            return True

        if screen == "random_menu":
            show_random_menu(bot, chat_id, message_id)
            return True

        if screen == "random_result":
            if tid is not None:
                show_random_result(
                    bot, chat_id, message_id, tid,
                    payload.get("filter_key", "full"),
                )
                return True

        if screen == "search_prompt":
            if tid is not None:
                show_search_prompt(bot, chat_id, message_id, tid)
                return True

        if screen == "search_results":
            query = payload.get("query", "")
            if query:
                show_search_results(bot, chat_id, message_id, user_id, query)
                return True

        if screen == "settings":
            show_settings(bot, chat_id, message_id, user_id)
            return True

        if screen == "settings_permanent":
            show_permanent(bot, chat_id, message_id, user_id, payload.get("page", 1))
            return True

        if screen == "settings_servings":
            show_servings(bot, chat_id, message_id, user_id)
            return True

        if screen == "settings_diet":
            show_diet(bot, chat_id, message_id, user_id)
            return True

        if screen == "profile":
            from database.repositories.users import UsersRepository
            user = UsersRepository().get_by_id(user_id)
            if user:
                show_profile(bot, chat_id, message_id, user)
                return True

        if screen == "admin_main":
            show_admin_dashboard(bot, chat_id, message_id)
            return True

        if screen == "admin_page":
            from bot.handlers.admin import show_admin_subpage
            show_admin_subpage(bot, chat_id, message_id, payload.get("action", "stats"))
            return True

    except Exception as e:
        logger.exception("render_screen failed: %s / %s — %s", screen, payload, e)

    return False


def handle_back(bot: TeleBot, chat_id: int, message_id: int, user_id: int, telegram_id: int) -> None:
    entry = nav_service.pop_and_get(user_id)
    if entry:
        ok = render_screen(
            bot, chat_id, message_id, user_id,
            entry["screen"], entry.get("payload") or {}, telegram_id,
        )
        if ok:
            return
    nav_service.clear(user_id)
    nav_service.set_current(user_id, "home", {})
    show_main_menu(bot, chat_id, message_id)


def handle_home(bot: TeleBot, chat_id: int, message_id: int, user_id: int, telegram_id: int | None = None) -> None:
    from states.user_state import state_manager
    if telegram_id is not None:
        state_manager.clear(telegram_id)
    nav_service.clear(user_id)
    nav_service.set_current(user_id, "home", {})
    show_main_menu(bot, chat_id, message_id)

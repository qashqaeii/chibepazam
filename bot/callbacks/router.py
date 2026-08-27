from telebot import TeleBot

from bot.handlers import start, main_menu, pantry, recipe_handler, random_food
from bot.handlers import search, favorites, history, profile, settings, admin, decision, shopping, panel
from utils.logger import setup_logger

logger = setup_logger(__name__)


def register_all_handlers(bot: TeleBot) -> None:
    start.register_start_handlers(bot)
    main_menu.register_menu_handlers(bot)
    pantry.register_pantry_handlers(bot)
    recipe_handler.register_recipe_handlers(bot)
    random_food.register_random_handlers(bot)
    search.register_search_handlers(bot)
    favorites.register_favorites_handlers(bot)
    history.register_history_handlers(bot)
    profile.register_profile_handlers(bot)
    settings.register_settings_handlers(bot)
    admin.register_admin_handlers(bot)
    decision.register_decision_handlers(bot)
    shopping.register_shopping_handlers(bot)
    panel.register_panel_handlers(bot)
    logger.info("All handlers registered")

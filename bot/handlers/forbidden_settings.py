from telebot import TeleBot

from bot.handlers.base import safe_edit
from bot.keyboards.recipe import forbidden_keyboard
from database.repositories.settings import SettingsRepository
from services.ingredient_service import IngredientService
from utils.screen import build_screen
from utils.menu_style import status_chip


settings_repo = SettingsRepository()
ingredient_service = IngredientService()


def show_forbidden(bot: TeleBot, chat_id: int, message_id: int, user_id: int, page: int = 1) -> None:
    ingredients = ingredient_service.get_all_active()
    selected = settings_repo.get_forbidden_ids(user_id)
    from utils.pagination import paginate
    from config import Config

    _, current_page, total_pages = paginate(ingredients, page, Config.INGREDIENTS_PER_PAGE)
    text = build_screen(
        emoji="🚫",
        title="مواد غیرمجاز",
        description=[
            "موادی که نمی‌خوری، حساسیت داری یا نمی‌توانی بخوری.",
            "غذاهای حاوی این مواد در پیشنهادها نمایش داده نمی‌شوند.",
        ],
        details=[
            status_chip("انتخاب‌شده", len(selected), "🚫"),
            "💡  برای حذف، دوباره روی همان ماده بزن",
        ],
        footer="👇 روی ماده بزن تا انتخاب/حذف شود",
    )
    safe_edit(
        bot, chat_id, message_id, text,
        forbidden_keyboard(ingredients, selected, page, total_pages),
    )

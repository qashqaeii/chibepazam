from telebot import TeleBot

from bot.handlers.base import safe_edit
from bot.keyboards.main import profile_keyboard
from utils.telegram import esc


def show_profile(bot: TeleBot, chat_id: int, message_id: int, user: dict) -> None:
    from services.ingredient_service import IngredientService
    from database.repositories.favorites import FavoritesRepository

    pantry_count = IngredientService().pantry_count(user["id"])
    fav_count = len(FavoritesRepository().get_all(user["id"]))

    name = esc(user.get("first_name") or "کاربر")
    username = f"@{esc(user['username'])}" if user.get("username") else "—"

    text = (
        f"👤 <b>حساب من</b>\n\n"
        f"نام: {name}\n"
        f"یوزرنیم: {username}\n\n"
        f"🧺 مواد انتخاب‌شده: {pantry_count}\n"
        f"❤️ علاقه‌مندی‌ها: {fav_count}\n"
        f"📅 عضو از: {user.get('created_at', '—')}"
    )
    safe_edit(bot, chat_id, message_id, text, profile_keyboard())


def register_profile_handlers(bot: TeleBot) -> None:
    pass

from telebot import TeleBot

from bot.handlers.base import safe_edit
from bot.keyboards.main import profile_keyboard
from utils.screen import build_screen
from utils.telegram import esc


def show_profile(bot: TeleBot, chat_id: int, message_id: int, user: dict) -> None:
    from services.ingredient_service import IngredientService
    from services.cooked_service import CookedService
    from database.repositories.favorites import FavoritesRepository

    uid = user["id"]
    pantry_count = IngredientService().pantry_count(uid)
    fav_count = len(FavoritesRepository().get_all(uid))
    permanent = len(IngredientService().get_permanent_ids(uid))
    cooked = CookedService().stats_for_user(uid)

    name = esc(user.get("first_name") or "کاربر")
    username = f"@{esc(user['username'])}" if user.get("username") else "—"
    joined = user.get("created_at", "—")
    if hasattr(joined, "strftime"):
        joined = joined.strftime("%Y/%m/%d")

    text = build_screen(
        emoji="👤",
        title="حساب من",
        description=[
            f"سلام <b>{name}</b>! 👋",
            "خلاصه فعالیت تو در ربات:",
        ],
        details=[
            f"🔗  یوزرنیم: {username}",
            f"🧺  مواد انتخاب‌شده: <b>{pantry_count}</b>",
            f"🏠  مواد همیشگی: <b>{permanent}</b>",
            f"❤️  علاقه‌مندی‌ها: <b>{fav_count}</b>",
            f"🍽  پخته‌شده: <b>{cooked['total_cooks']}</b> بار ({cooked['distinct_recipes']} غذا)",
            f"📅  عضو از: {joined}",
        ],
        footer="👇 برای بازگشت از دکمه پایین استفاده کن",
    )
    safe_edit(bot, chat_id, message_id, text, profile_keyboard())


def register_profile_handlers(bot: TeleBot) -> None:
    pass

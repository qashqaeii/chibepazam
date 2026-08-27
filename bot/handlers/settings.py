from telebot import TeleBot

from bot.handlers.base import safe_edit, answer_callback
from bot.keyboards.settings_kb import (
    settings_keyboard,
    servings_keyboard,
    diet_keyboard,
    permanent_keyboard,
)
from database.repositories.settings import SettingsRepository
from services.ingredient_service import IngredientService
from services.nav_service import nav_service
from utils.telegram import esc


settings_repo = SettingsRepository()
ingredient_service = IngredientService()

DIET_LABELS = {
    "none": "بدون محدودیت",
    "vegetarian": "گیاهخواری",
    "vegan": "وگان",
}


def show_settings(bot: TeleBot, chat_id: int, message_id: int, user_id: int) -> None:
    settings = settings_repo.get(user_id) or {"servings": 4, "notifications": 1, "diet_type": "none"}
    text = (
        "⚙️ <b>تنظیمات</b>\n\n"
        "تنظیمات «غذا چی بپزم؟»\n\n"
        f"👨‍👩‍👧 تعداد نفرات: {settings.get('servings', 4)}\n"
        f"🌱 رژیم: {DIET_LABELS.get(settings.get('diet_type', 'none'), '—')}"
    )
    safe_edit(
        bot,
        chat_id,
        message_id,
        text,
        settings_keyboard(bool(settings.get("notifications", 1))),
    )


def show_permanent(bot: TeleBot, chat_id: int, message_id: int, user_id: int, page: int = 1) -> None:
    ingredients = ingredient_service.get_common_for_permanent()
    selected = ingredient_service.get_permanent_ids(user_id)
    from utils.pagination import paginate
    from config import Config

    _, current_page, total_pages = paginate(ingredients, page, Config.INGREDIENTS_PER_PAGE)
    text = (
        "🏠 <b>مواد همیشگی من</b>\n\n"
        "موادی که همیشه توی خونه داری رو انتخاب کن.\n"
        "این‌ها خودکار در پیشنهادها لحاظ می‌شن 👇"
    )
    safe_edit(
        bot,
        chat_id,
        message_id,
        text,
        permanent_keyboard(ingredients, selected, page, total_pages),
    )


def show_servings(bot: TeleBot, chat_id: int, message_id: int, user_id: int) -> None:
    settings = settings_repo.get(user_id)
    current = settings.get("servings", 4) if settings else 4
    text = "👨‍👩‍👧 <b>تعداد نفرات</b>\n\nچند نفر غذا می‌خوری؟"
    safe_edit(bot, chat_id, message_id, text, servings_keyboard(current))


def show_diet(bot: TeleBot, chat_id: int, message_id: int, user_id: int) -> None:
    settings = settings_repo.get(user_id)
    current = settings.get("diet_type", "none") if settings else "none"
    text = "🌱 <b>رژیم غذایی</b>\n\nنوع رژیمت رو انتخاب کن:"
    safe_edit(bot, chat_id, message_id, text, diet_keyboard(current))


def register_settings_handlers(bot: TeleBot) -> None:
    from services.user_service import UserService
    user_service = UserService()

    @bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("settings:"))
    def handle_settings(call):
        answer_callback(bot, call)
        user = user_service.get_user(call.from_user.id)
        if not user:
            return

        user_id = user["id"]
        chat_id = call.message.chat.id
        msg_id = call.message.message_id
        parts = call.data.split(":")

        if parts[1] == "permanent":
            nav_service.navigate(user_id, "settings_permanent", {"page": 1})
            show_permanent(bot, chat_id, msg_id, user_id)

        elif parts[1] == "perm":
            ingredient_id = int(parts[2])
            page = int(parts[3]) if len(parts) > 3 else 1
            ingredient_service.toggle_permanent(user_id, ingredient_id)
            nav_service.replace(user_id, "settings_permanent", {"page": page})
            show_permanent(bot, chat_id, msg_id, user_id, page)

        elif parts[1] == "servings":
            if len(parts) > 2:
                settings_repo.update_servings(user_id, int(parts[2]))
                show_settings(bot, chat_id, msg_id, user_id)
            else:
                nav_service.navigate(user_id, "settings_servings", {})
                show_servings(bot, chat_id, msg_id, user_id)

        elif parts[1] == "diet":
            if len(parts) > 2:
                settings_repo.update_diet(user_id, parts[2])
                show_settings(bot, chat_id, msg_id, user_id)
            else:
                nav_service.navigate(user_id, "settings_diet", {})
                show_diet(bot, chat_id, msg_id, user_id)

        elif parts[1] == "notifications":
            new_val = settings_repo.toggle_notifications(user_id)
            answer_callback(bot, call, "🔔 روشن شد" if new_val else "🔕 خاموش شد")
            show_settings(bot, chat_id, msg_id, user_id)

        elif parts[1] == "forbidden":
            text = "🚫 <b>مواد غیرمجاز</b>\n\nاین قابلیت به زودی فعال می‌شود."
            from bot.keyboards.navigation import nav_row
            from telebot import types
            kb = types.InlineKeyboardMarkup()
            kb.row(*nav_row())
            safe_edit(bot, chat_id, msg_id, text, kb)

        else:
            show_settings(bot, chat_id, msg_id, user_id)

    @bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("page:perm:"))
    def handle_perm_page(call):
        answer_callback(bot, call)
        user = user_service.get_user(call.from_user.id)
        if not user:
            return
        page = int(call.data.split(":")[2])
        nav_service.replace(user["id"], "settings_permanent", {"page": page})
        show_permanent(bot, call.message.chat.id, call.message.message_id, user["id"], page)

from telebot import TeleBot

from bot.handlers.base import safe_edit, answer_callback
from bot.keyboards.random_kb import random_menu_keyboard, random_result_keyboard
from services.random_service import RandomService
from services.user_service import UserService
from services.nav_service import nav_service
from database.repositories.events import EventsRepository
from utils.screen import build_screen, ACTION_FOOTER
from utils.telegram import esc, difficulty_label, cost_label


random_service = RandomService()
user_service = UserService()
events_repo = EventsRepository()

_last_random: dict[int, dict] = {}
_last_filter: dict[int, str] = {}

FILTER_LABELS = {
    "full": "🎲  کاملاً شانسی",
    "fast": "⚡  سریع",
    "cheap": "💰  اقتصادی",
    "chicken": "🍗  با مرغ",
    "meat": "🥩  گوشتی",
    "vegetarian": "🌱  بدون گوشت",
    "rice": "🍚  برنجی",
    "bread": "🥖  نونی",
    "traditional": "🥘  سنتی",
}


def show_random_menu(bot: TeleBot, chat_id: int, message_id: int) -> None:
    text = build_screen(
        emoji="🎲",
        title="امروز چی بپزم؟",
        description=[
            "نمیدونی چی بپزی؟ بذار انتخاب کنم!",
            "یک فیلتر انتخاب کن یا کاملاً شانسی برو.",
        ],
        details=[
            "⚡  سریع  ·  💰  اقتصادی  ·  🌱  گیاهی",
            "🍗  مرغ  ·  🥩  گوشت  ·  🍚  برنجی",
        ],
    )
    safe_edit(bot, chat_id, message_id, text, random_menu_keyboard())


def show_random_result(bot: TeleBot, chat_id: int, message_id: int, telegram_id: int, filter_key: str = "full") -> None:
    exclude = []
    if telegram_id in _last_random and filter_key == _last_filter.get(telegram_id, "full"):
        exclude = [_last_random[telegram_id]["id"]]

    user = user_service.get_user(telegram_id)
    user_id = user["id"] if user else None
    recipe = random_service.get_random(filter_key, exclude, user_id=user_id)
    if not recipe:
        text = build_screen(
            emoji="🎲",
            title="پیشنهاد شانسی",
            description=[
                "متأسفانه غذایی با این فیلتر پیدا نشد.",
                "فیلتر دیگه‌ای امتحان کن.",
            ],
        )
        safe_edit(bot, chat_id, message_id, text, random_menu_keyboard())
        return

    _last_random[telegram_id] = recipe
    _last_filter[telegram_id] = filter_key

    user = user_service.get_user(telegram_id)
    if user:
        events_repo.log("random", user["id"], {"filter": filter_key, "recipe_id": recipe["id"]})

    total_time = recipe.get("prep_time", 0) + recipe.get("cook_time", 0)
    filter_label = FILTER_LABELS.get(filter_key, "🎲  شانسی")
    desc = recipe.get("description") or "یک پیشنهاد خوش‌طعم برای امروزت"

    text = build_screen(
        emoji="🎲",
        title="پیشنهاد شانسی",
        description=[
            f"{recipe.get('emoji', '🍲')}  <b>{esc(recipe['name'])}</b>",
            desc[:100] + ("…" if len(desc) > 100 else ""),
        ],
        details=[
            f"🏷  فیلتر: {filter_label}",
            f"⏱  زمان: <b>{total_time}</b> دقیقه",
            f"💰  هزینه: {cost_label(recipe.get('cost_level', 'medium'))}",
            f"👨‍🍳  سختی: {difficulty_label(recipe.get('difficulty', 'medium'))}",
        ],
        footer=ACTION_FOOTER,
        escape_title=False,
    )
    safe_edit(bot, chat_id, message_id, text, random_result_keyboard(recipe["id"]))


def register_random_handlers(bot: TeleBot) -> None:
    @bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("random:"))
    def handle_random(call):
        answer_callback(bot, call, "🎲 دارم انتخاب می‌کنم...")
        chat_id = call.message.chat.id
        msg_id = call.message.message_id
        telegram_id = call.from_user.id
        user = user_service.get_user(telegram_id)
        action = call.data.split(":")[1]

        if action == "next":
            filter_key = _last_filter.get(telegram_id, "full")
        else:
            filter_key = action
            if user and action != "next":
                nav_service.navigate(user["id"], "random_result", {"filter_key": filter_key})

        show_random_result(bot, chat_id, msg_id, telegram_id, filter_key)

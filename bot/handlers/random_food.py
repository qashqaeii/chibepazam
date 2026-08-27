from telebot import TeleBot

from bot.handlers.base import safe_edit, answer_callback
from bot.keyboards.random_kb import random_menu_keyboard, random_result_keyboard
from services.random_service import RandomService
from services.user_service import UserService
from services.nav_service import nav_service
from database.repositories.events import EventsRepository
from utils.telegram import esc, difficulty_label, cost_label


random_service = RandomService()
user_service = UserService()
events_repo = EventsRepository()

_last_random: dict[int, dict] = {}
_last_filter: dict[int, str] = {}


def show_random_menu(bot: TeleBot, chat_id: int, message_id: int) -> None:
    text = (
        "🎲 <b>امروز چی بپزم؟</b>\n\n"
        "چه نوع پیشنهادی دوست داری؟"
    )
    safe_edit(bot, chat_id, message_id, text, random_menu_keyboard())


def show_random_result(bot: TeleBot, chat_id: int, message_id: int, telegram_id: int, filter_key: str = "full") -> None:
    exclude = []
    if telegram_id in _last_random and filter_key == _last_filter.get(telegram_id, "full"):
        exclude = [_last_random[telegram_id]["id"]]

    recipe = random_service.get_random(filter_key, exclude)
    if not recipe:
        text = "🎲 متأسفانه غذایی پیدا نشد.\nفیلتر دیگه‌ای امتحان کن 👇"
        safe_edit(bot, chat_id, message_id, text, random_menu_keyboard())
        return

    _last_random[telegram_id] = recipe
    _last_filter[telegram_id] = filter_key

    user = user_service.get_user(telegram_id)
    if user:
        events_repo.log("random", user["id"], {"filter": filter_key, "recipe_id": recipe["id"]})

    total_time = recipe.get("prep_time", 0) + recipe.get("cook_time", 0)
    text = (
        "🎲 <b>پیشنهاد من:</b>\n\n"
        f"{recipe.get('emoji', '🍲')} <b>{esc(recipe['name'])}</b>\n\n"
        f"⏱ حدود {total_time} دقیقه\n"
        f"💰 {cost_label(recipe.get('cost_level', 'medium'))}\n"
        f"👨‍🍳 {difficulty_label(recipe.get('difficulty', 'medium'))}"
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

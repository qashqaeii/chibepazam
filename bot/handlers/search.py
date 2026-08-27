from telebot import TeleBot, types

from bot.handlers.base import safe_edit
from bot.keyboards.random_kb import search_prompt_keyboard
from bot.keyboards.recipe import recipe_list_keyboard
from bot.keyboards.navigation import nav_row
from services.search_service import SearchService
from services.user_service import UserService
from services.nav_service import nav_service
from states.user_state import UserState, state_manager
from utils.telegram import esc


search_service = SearchService()
user_service = UserService()


def show_search_prompt(bot: TeleBot, chat_id: int, message_id: int, telegram_id: int) -> None:
    state_manager.set_state(
        telegram_id, UserState.WAITING_SEARCH,
        chat_id=chat_id, message_id=message_id,
    )
    text = (
        "🔍 <b>جستجوی غذا</b>\n\n"
        "اسم غذا یا یکی از موادش رو برام بنویس.\n\n"
        "مثلاً:\n"
        "قورمه سبزی\n"
        "مرغ\n"
        "بادمجان"
    )
    safe_edit(bot, chat_id, message_id, text, search_prompt_keyboard())


def show_search_results(bot: TeleBot, chat_id: int, message_id: int, user_id: int, query: str) -> None:
    results = search_service.search(user_id, query)
    if not results:
        text = f"🔍 نتیجه‌ای برای «{esc(query)}» پیدا نشد."
        kb = types.InlineKeyboardMarkup()
        kb.row(*nav_row())
        safe_edit(bot, chat_id, message_id, text, kb)
        nav_service.replace(user_id, "search_results", {"query": query})
        return

    text = f"🔍 نتایج جستجو برای «{esc(query)}»:"
    safe_edit(bot, chat_id, message_id, text, recipe_list_keyboard(results))
    nav_service.replace(user_id, "search_results", {"query": query})


def register_search_handlers(bot: TeleBot) -> None:
    @bot.message_handler(func=lambda m: state_manager.is_waiting(m.from_user.id, UserState.WAITING_SEARCH))
    def handle_search_query(message: types.Message):
        state_data = state_manager.get(message.from_user.id)
        state_manager.clear(message.from_user.id)

        user = user_service.get_user(message.from_user.id)
        if not user:
            return

        query = message.text.strip() if message.text else ""
        if len(query) < 2:
            bot.send_message(message.chat.id, "⚠️ حداقل ۲ حرف بنویس.", parse_mode="HTML")
            return

        chat_id = state_data.data.get("chat_id", message.chat.id)
        msg_id = state_data.data.get("message_id")

        if msg_id:
            nav_service.navigate(user["id"], "search_results", {"query": query})
            show_search_results(bot, chat_id, msg_id, user["id"], query)
        else:
            nav_service.navigate(user["id"], "search_results", {"query": query})
            results = search_service.search(user["id"], query)
            if not results:
                bot.send_message(message.chat.id, f"🔍 نتیجه‌ای برای «{esc(query)}» پیدا نشد.", parse_mode="HTML")
                return
            text = f"🔍 نتایج جستجو برای «{esc(query)}»:"
            bot.send_message(
                message.chat.id, text,
                reply_markup=recipe_list_keyboard(results),
                parse_mode="HTML",
            )

from telebot import TeleBot, types

from bot.handlers.base import answer_callback, show_main_menu
from bot.handlers.pantry import show_pantry_main
from bot.handlers.random_food import show_random_menu
from bot.handlers.search import show_search_prompt
from bot.handlers.favorites import show_favorites
from bot.handlers.history import show_history
from bot.handlers.profile import show_profile
from bot.handlers.settings import show_settings
from bot.handlers.navigation import handle_back
from services.user_service import UserService
from services.nav_service import nav_service


def register_menu_handlers(bot: TeleBot) -> None:
    user_service = UserService()

    @bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("menu:"))
    def handle_menu(call: types.CallbackQuery):
        answer_callback(bot, call)
        user = user_service.get_user(call.from_user.id)
        if not user:
            show_main_menu(bot, call.message.chat.id, call.message.message_id)
            return

        action = call.data.split(":", 1)[1]
        chat_id = call.message.chat.id
        msg_id = call.message.message_id
        uid = user["id"]

        screen_map = {
            "pantry": ("pantry_main", {}),
            "random": ("random_menu", {}),
            "search": ("search_prompt", {}),
            "favorites": ("favorites", {"page": 1}),
            "history": ("history", {}),
            "profile": ("profile", {}),
            "settings": ("settings", {}),
        }
        if action not in screen_map:
            return

        screen, payload = screen_map[action]
        nav_service.navigate(uid, screen, payload)

        handlers = {
            "pantry": lambda: show_pantry_main(bot, chat_id, msg_id, uid),
            "random": lambda: show_random_menu(bot, chat_id, msg_id),
            "search": lambda: show_search_prompt(bot, chat_id, msg_id, call.from_user.id),
            "favorites": lambda: show_favorites(bot, chat_id, msg_id, uid, 1),
            "history": lambda: show_history(bot, chat_id, msg_id, uid),
            "profile": lambda: show_profile(bot, chat_id, msg_id, user),
            "settings": lambda: show_settings(bot, chat_id, msg_id, uid),
        }
        handlers[action]()

    @bot.callback_query_handler(func=lambda c: c.data == "nav:back")
    def handle_nav_back(call: types.CallbackQuery):
        answer_callback(bot, call)
        user = user_service.get_user(call.from_user.id)
        if not user:
            show_main_menu(bot, call.message.chat.id, call.message.message_id)
            return
        handle_back(bot, call.message.chat.id, call.message.message_id, user["id"], call.from_user.id)

    @bot.callback_query_handler(func=lambda c: c.data == "noop")
    def handle_noop(call: types.CallbackQuery):
        answer_callback(bot, call)

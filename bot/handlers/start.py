from telebot import TeleBot, types

from bot.handlers.base import show_main_menu
from bot.handlers.navigation import handle_home
from bot.keyboards.main import main_menu_text, main_menu_keyboard
from services.user_service import UserService
from services.nav_service import nav_service
from database.repositories.events import EventsRepository
from utils.telegram import esc


def register_start_handlers(bot: TeleBot) -> None:
    user_service = UserService()
    events_repo = EventsRepository()

    @bot.message_handler(commands=["start"])
    def handle_start(message: types.Message):
        user = user_service.register(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
        events_repo.log("start", user["id"])

        saved = nav_service.get_current(user["id"])
        if saved and saved.get("screen") and saved["screen"] != "home":
            from bot.handlers.navigation import render_screen
            msg = bot.send_message(message.chat.id, "⏳", parse_mode="HTML")
            if render_screen(
                bot, message.chat.id, msg.message_id, user["id"],
                saved["screen"], saved.get("payload") or {},
                message.from_user.id,
            ):
                return

        nav_service.set_current(user["id"], "home", {})
        name = esc(message.from_user.first_name or "دوست")
        text = main_menu_text(greeting=f"سلام {name}! 👋")
        bot.send_message(
            message.chat.id,
            text,
            reply_markup=main_menu_keyboard(),
            parse_mode="HTML",
        )

    @bot.callback_query_handler(func=lambda c: c.data == "nav:home")
    def handle_nav_home(call: types.CallbackQuery):
        from bot.handlers.base import answer_callback

        answer_callback(bot, call)
        user = user_service.get_user(call.from_user.id)
        if user:
            handle_home(bot, call.message.chat.id, call.message.message_id, user["id"], call.from_user.id)
        else:
            show_main_menu(bot, call.message.chat.id, call.message.message_id)

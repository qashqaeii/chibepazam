"""Shared bot utilities for handlers."""

from telebot import TeleBot, types

from bot.keyboards.main import MAIN_MENU_TEXT, main_menu_keyboard
from bot.keyboards.navigation import error_keyboard
from utils.logger import setup_logger
from utils.telegram import esc

logger = setup_logger(__name__)


def safe_edit(
    bot: TeleBot,
    chat_id: int,
    message_id: int,
    text: str,
    reply_markup: types.InlineKeyboardMarkup | None = None,
    parse_mode: str = "HTML",
) -> bool:
    try:
        bot.edit_message_text(
            text,
            chat_id,
            message_id,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
        )
        return True
    except Exception as e:
        err = str(e).lower()
        if "message is not modified" in err or "exactly the same" in err:
            return True
        logger.warning("edit_message failed: %s", e)
        try:
            bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode=parse_mode)
        except Exception as send_err:
            logger.error("send_message fallback failed: %s", send_err)
        return False


def show_error(bot: TeleBot, call: types.CallbackQuery, retry_callback: str = "nav:home") -> None:
    safe_edit(
        bot,
        call.message.chat.id,
        call.message.message_id,
        "⚠️ یه مشکلی پیش اومد.\n\nلطفاً دوباره امتحان کن 👇",
        error_keyboard(retry_callback),
    )


def show_main_menu(bot: TeleBot, chat_id: int, message_id: int) -> None:
    safe_edit(bot, chat_id, message_id, MAIN_MENU_TEXT, main_menu_keyboard())


def answer_callback(bot: TeleBot, call: types.CallbackQuery, text: str | None = None) -> None:
    from database.repositories.events import EventsRepository

    if call.from_user:
        allowed = EventsRepository().check_rate_limit(
            call.from_user.id, "callback", max_count=40, seconds=10
        )
        if not allowed:
            try:
                bot.answer_callback_query(call.id, "⏳ کمی صبر کن...", show_alert=False)
            except Exception:
                pass
            return
    try:
        bot.answer_callback_query(call.id, text=text, show_alert=False)
    except Exception as e:
        err = str(e).lower()
        if "query is too old" not in err and "already been answered" not in err:
            logger.debug("answer_callback_query failed: %s", e)

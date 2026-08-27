import sys
import telebot
from telebot import apihelper

from config import Config
from database.connection import init_pool
from bot.callbacks.router import register_all_handlers
from utils.logger import setup_logger

logger = setup_logger("main")


def main() -> None:
    try:
        Config.validate()
    except ValueError as e:
        logger.error(str(e))
        sys.exit(1)

    try:
        init_pool()
    except Exception as e:
        logger.error("Database connection failed: %s", e)
        sys.exit(1)

    bot = telebot.TeleBot(Config.BOT_TOKEN, parse_mode="HTML")
    register_all_handlers(bot)

    logger.info("Bot started — «غذا چی بپزم؟»")
    bot.infinity_polling(timeout=30, long_polling_timeout=30, skip_pending=True)


if __name__ == "__main__":
    main()

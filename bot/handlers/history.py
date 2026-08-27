from telebot import TeleBot

from bot.handlers.base import safe_edit
from bot.keyboards.navigation import nav_row
from telebot import types
from database.repositories.history import HistoryRepository
from utils.telegram import esc


history_repo = HistoryRepository()


def show_history(bot: TeleBot, chat_id: int, message_id: int, user_id: int) -> None:
    items = history_repo.get_recent(user_id, 10)
    if not items:
        text = (
            "🕘 <b>غذاهایی که اخیراً دیدی</b>\n\n"
            "هنوز تاریخچه‌ای نداری."
        )
    else:
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        lines = "\n".join(
            f"{emojis[i]} {esc(r['name'])}" for i, r in enumerate(items)
        )
        text = f"🕘 <b>غذاهایی که اخیراً دیدی</b>\n\n{lines}"

    kb = types.InlineKeyboardMarkup(row_width=1)
    for r in items[:5]:
        kb.add(types.InlineKeyboardButton(
            f"{r.get('emoji', '🍲')} {r['name']}",
            callback_data=f"recipe:view:{r['id']}",
        ))
    kb.row(*nav_row())
    safe_edit(bot, chat_id, message_id, text, kb)


def register_history_handlers(bot: TeleBot) -> None:
    pass

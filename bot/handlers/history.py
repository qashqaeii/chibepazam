from telebot import TeleBot

from bot.handlers.base import safe_edit
from bot.keyboards.builder import btn, append_nav
from telebot import types
from database.repositories.history import HistoryRepository
from utils.screen import build_screen, list_body
from utils.telegram import esc


history_repo = HistoryRepository()


def show_history(bot: TeleBot, chat_id: int, message_id: int, user_id: int) -> None:
    items = history_repo.get_recent(user_id, 10)
    if not items:
        text = build_screen(
            emoji="🕘",
            title="تاریخچه بازدید",
            description=[
                "غذاهایی که اخیراً مشاهده کردی اینجا ذخیره می‌شوند.",
                "برای بازدید دوباره روی نام غذا بزن.",
            ],
        )
    else:
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        lines = [f"{emojis[i]}  {r.get('emoji', '🍲')} {esc(r['name'])}" for i, r in enumerate(items)]
        text = build_screen(
            emoji="🕘",
            title="غذاهایی که اخیراً دیدی",
            description=f"آخرین <b>{len(items)}</b> غذای مشاهده‌شده:",
            body=list_body(lines),
            footer="👇 برای مشاهده دوباره بزن",
        )

    kb = types.InlineKeyboardMarkup(row_width=1)
    for r in items[:5]:
        kb.add(btn(f"{r.get('emoji', '🍲')}  {r['name']}", f"recipe:view:{r['id']}"))
    append_nav(kb)
    safe_edit(bot, chat_id, message_id, text, kb)


def register_history_handlers(bot: TeleBot) -> None:
    pass

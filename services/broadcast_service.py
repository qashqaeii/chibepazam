import time
from telebot import TeleBot, types

from database.repositories.users import UsersRepository


class BroadcastService:
    BATCH_SIZE = 25
    BATCH_DELAY = 1.0

    def __init__(self):
        self.users = UsersRepository()

    def recipient_count(self) -> int:
        return len(self.users.get_active_telegram_ids())

    def send(
        self,
        bot: TeleBot,
        text: str,
        photo_file_id: str | None = None,
        button_text: str | None = None,
        button_url: str | None = None,
    ) -> tuple[int, int]:
        ids = self.users.get_active_telegram_ids()
        ok = fail = 0
        markup = None
        if button_text and button_url:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(button_text, url=button_url))

        for i, tid in enumerate(ids):
            try:
                if photo_file_id:
                    bot.send_photo(tid, photo_file_id, caption=text, parse_mode="HTML", reply_markup=markup)
                else:
                    bot.send_message(tid, text, parse_mode="HTML", reply_markup=markup, disable_web_page_preview=True)
                ok += 1
            except Exception:
                fail += 1
            if (i + 1) % self.BATCH_SIZE == 0:
                time.sleep(self.BATCH_DELAY)
        return ok, fail

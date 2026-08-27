from telebot import TeleBot

from bot.handlers.base import safe_edit
from bot.keyboards.recipe import favorites_keyboard
from database.repositories.favorites import FavoritesRepository
from config import Config
from utils.pagination import paginate
from utils.telegram import esc
from services.nav_service import nav_service


favorites_repo = FavoritesRepository()


def show_favorites(bot: TeleBot, chat_id: int, message_id: int, user_id: int, page: int = 1) -> None:
    all_favs = favorites_repo.get_all(user_id)
    page_items, current_page, total_pages = paginate(all_favs, page, Config.FAVORITES_PER_PAGE)

    if not page_items:
        text = (
            "❤️ <b>غذاهای موردعلاقه</b>\n\n"
            "هنوز غذایی ذخیره نکردی.\n"
            "روی ❤️ ذخیره در صفحه غذا بزن 👇"
        )
    else:
        lines = "\n".join(
            f"{r.get('emoji', '🍲')} {esc(r['name'])}" for r in page_items
        )
        text = f"❤️ <b>غذاهای موردعلاقه</b>\n\n{lines}"

    safe_edit(bot, chat_id, message_id, text, favorites_keyboard(page_items, current_page, total_pages))


def register_favorites_handlers(bot: TeleBot) -> None:
    from bot.handlers.base import answer_callback
    from services.user_service import UserService

    user_service = UserService()

    @bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("page:fav:"))
    def handle_fav_page(call):
        answer_callback(bot, call)
        user = user_service.get_user(call.from_user.id)
        if not user:
            return
        page = int(call.data.split(":")[2])
        nav_service.replace(user["id"], "favorites", {"page": page})
        show_favorites(bot, call.message.chat.id, call.message.message_id, user["id"], page)

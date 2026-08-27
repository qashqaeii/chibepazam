from telebot import TeleBot, types

from bot.handlers.base import safe_edit, answer_callback
from bot.keyboards.builder import btn, append_nav
from services.shopping_service import ShoppingService
from services.user_service import UserService
from services.nav_service import nav_service
from utils.screen import build_screen, ACTION_FOOTER
from utils.shopping import build_share_url


shopping_service = ShoppingService()
user_service = UserService()


def show_cart(bot: TeleBot, chat_id: int, message_id: int, user_id: int) -> None:
    count = shopping_service.count(user_id)
    if count == 0:
        text = build_screen(
            emoji="🛒",
            title="لیست خرید ترکیبی",
            description=[
                "چند غذا را انتخاب کن تا مواد مشترک را یکجا ببینی.",
                "از صفحه هر غذا «افزودن به لیست خرید» را بزن.",
            ],
            details=[
                "💡  مواد تکراری خودکار جمع می‌شوند",
                "📤  می‌توانی لیست را برای خریدار بفرستی",
            ],
            footer="👇 بعد از افزودن غذا، دوباره اینجا بیا",
        )
        safe_edit(bot, chat_id, message_id, text, append_nav(types.InlineKeyboardMarkup()))
        return

    plain, items = shopping_service.build_merged_list(user_id)
    text = build_screen(
        emoji="🛒",
        title="لیست خرید ترکیبی",
        description=[
            f"<b>{count}</b> غذا در لیست — <b>{len(items)}</b> ماده برای خرید",
            "مواد مشابه با هم جمع شده‌اند.",
        ],
        body=plain.split("────────────", 1)[-1].strip() if "────────────" in plain else plain,
        footer=ACTION_FOOTER,
    )
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(btn("📤  ارسال لیست", "shop:send"))
    kb.add(btn("🗑  پاک کردن لیست", "shop:clear:ask"))
    append_nav(kb)
    safe_edit(bot, chat_id, message_id, text, kb)


def register_shopping_handlers(bot: TeleBot) -> None:
    @bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("shop:"))
    def handle_shop(call):
        user = user_service.get_user(call.from_user.id)
        if not user:
            answer_callback(bot, call)
            return
        uid = user["id"]
        chat_id = call.message.chat.id
        msg_id = call.message.message_id
        action = call.data.split(":")[1]

        if action == "cart":
            answer_callback(bot, call)
            nav_service.navigate(uid, "shopping_cart", {})
            show_cart(bot, chat_id, msg_id, uid)
        elif action == "send":
            text, _ = shopping_service.build_merged_list(uid)
            try:
                bot_username = bot.get_me().username or "Chibepazamrobot"
            except Exception:
                bot_username = "Chibepazamrobot"
            url = build_share_url(text, bot_username)
            answer_callback(bot, call, "لیست آماده شد ✅")
            kb = types.InlineKeyboardMarkup()
            if url:
                kb.add(types.InlineKeyboardButton("📲  ارسال به خریدار", url=url))
            bot.send_message(chat_id, text, reply_markup=kb, disable_web_page_preview=True)
        elif action == "clear":
            if len(call.data.split(":")) > 2 and call.data.split(":")[2] == "yes":
                shopping_service.clear(uid)
                answer_callback(bot, call, "لیست پاک شد")
                show_cart(bot, chat_id, msg_id, uid)
            else:
                answer_callback(bot, call)
                text = build_screen(
                    emoji="🗑",
                    title="پاک کردن لیست خرید",
                    description=[
                        "همه غذاها از لیست خرید حذف شوند؟",
                        "این عمل قابل بازگشت نیست.",
                    ],
                    footer="👇 تأیید یا انصراف",
                )
                kb = types.InlineKeyboardMarkup()
                kb.row(btn("✅  بله، پاک کن", "shop:clear:yes"), btn("❌  انصراف", "shop:cart"))
                safe_edit(bot, chat_id, msg_id, text, kb)

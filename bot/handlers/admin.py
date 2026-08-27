from telebot import TeleBot, types

from bot.handlers.base import safe_edit, answer_callback
from bot.keyboards.admin import (
    admin_dashboard_keyboard,
    admin_back_keyboard,
    admin_confirm_keyboard,
    admin_broadcast_preview_keyboard,
    admin_recipes_keyboard,
    admin_ingredients_keyboard,
    admin_categories_keyboard,
    admin_substitutes_keyboard,
)
from services.user_service import UserService
from services.admin_service import AdminService
from services.broadcast_service import BroadcastService
from states.user_state import UserState, state_manager
from utils.screen import build_screen, ACTION_FOOTER


user_service = UserService()
admin_service = AdminService()
broadcast_service = BroadcastService()


def show_admin_dashboard(bot: TeleBot, chat_id: int, message_id: int) -> None:
    dash = admin_service.analytics.dashboard()
    text = build_screen(
        emoji="👑",
        title="پنل مدیریت",
        description="خلاصه وضعیت ربات «غذا چی بپزم؟»",
        details=[
            f"📊  کاربران: <b>{dash['total_users']:,}</b>",
            f"🟢  DAU: <b>{dash['dau']:,}</b>",
            f"🍲  غذاها: <b>{admin_service.recipes.count_all():,}</b>",
            f"🥕  مواد: <b>{admin_service.ingredients.count_all():,}</b>",
            f"🔎  جستجوی امروز: <b>{dash['searches_today']:,}</b>",
            f"🎲  شانسی امروز: <b>{dash['random_today']:,}</b>",
            f"🍽  پخته‌شده: <b>{dash['cooked_total']:,}</b>",
        ],
        footer=ACTION_FOOTER,
    )
    safe_edit(bot, chat_id, message_id, text, admin_dashboard_keyboard())


def show_admin_subpage(
    bot: TeleBot, chat_id: int, message_id: int, action: str, page: int = 1, extra: dict | None = None,
) -> None:
    extra = extra or {}
    if action == "stats":
        d = admin_service.analytics.dashboard()
        top_r = "\n".join(
            f"{i+1}. {p.get('emoji','🍲')} {p['name']} — {p['fav_count']} ❤️"
            for i, p in enumerate(d["top_recipes"])
        ) or "—"
        top_i = "\n".join(
            f"{i+1}. {p.get('emoji','🥕')} {p['name']} — {p['cnt']}"
            for i, p in enumerate(d["top_ingredients"])
        ) or "—"
        top_s = "\n".join(
            f"{i+1}. {p['query']} — {p['cnt']}"
            for i, p in enumerate(d["top_searches"])
        ) or "—"
        text = build_screen(
            emoji="📊",
            title="داشبورد Analytics",
            details=[
                f"👥 کل کاربران: <b>{d['total_users']:,}</b>",
                f"🟢 DAU: <b>{d['dau']:,}</b>",
                f"🔎 جستجو امروز: <b>{d['searches_today']:,}</b>",
                f"🎲 Random امروز: <b>{d['random_today']:,}</b>",
                f"❤️ علاقه‌مندی‌ها: <b>{d['favorites_total']:,}</b>",
                f"🍽 پخته‌شده: <b>{d['cooked_total']:,}</b>",
                "",
                "<b>محبوب‌ترین غذاها</b>",
                top_r,
                "",
                "<b>مواد پرکاربرد</b>",
                top_i,
                "",
                "<b>جستجوهای برتر</b>",
                top_s,
            ],
            footer=ACTION_FOOTER,
        )
        safe_edit(bot, chat_id, message_id, text, admin_back_keyboard())
    elif action == "popular":
        popular = admin_service.analytics.favorites.count_popular(10)
        lines = "هنوز داده‌ای نیست." if not popular else "\n".join(
            f"{i+1}. {p.get('emoji', '🍲')} {p['name']} — {p['fav_count']} ❤️"
            for i, p in enumerate(popular)
        )
        safe_edit(bot, chat_id, message_id, f"❤️ <b>محبوب‌ترین غذاها</b>\n\n{lines}", admin_back_keyboard())
    elif action == "users":
        d = admin_service.analytics.dashboard()
        text = build_screen(
            emoji="👥",
            title="کاربران",
            details=[
                f"تعداد کل: <b>{d['total_users']:,}</b>",
                f"فعال امروز: <b>{d['dau']:,}</b>",
            ],
        )
        safe_edit(bot, chat_id, message_id, text, admin_back_keyboard())
    elif action == "recipes":
        items, cur, total = admin_service.recipes.list_page(page, 12)
        text = build_screen(
            emoji="🍲",
            title="مدیریت غذاها",
            description=f"صفحه {cur} از {total} — روی غذا بزن برای فعال/غیرفعال",
            footer=ACTION_FOOTER,
        )
        safe_edit(bot, chat_id, message_id, text, admin_recipes_keyboard(items, cur, total))
    elif action == "ingredients":
        items, cur, total = admin_service.ingredients.list_page(page, 16)
        text = build_screen(
            emoji="🥕",
            title="مدیریت مواد",
            description=f"صفحه {cur} از {total}",
            footer=ACTION_FOOTER,
        )
        safe_edit(bot, chat_id, message_id, text, admin_ingredients_keyboard(items, cur, total))
    elif action == "categories":
        cats = admin_service.categories.get_all()
        text = build_screen(
            emoji="📂",
            title="دسته‌بندی غذاها",
            description="روی دسته بزن برای فعال/غیرفعال",
        )
        safe_edit(bot, chat_id, message_id, text, admin_categories_keyboard(cats))
    elif action == "substitutes":
        subs = admin_service.substitutes.list_all(30)
        text = build_screen(
            emoji="🔄",
            title="جایگزین مواد",
            description=f"{len(subs)} رکورد — برای حذف روی مورد بزن",
        )
        safe_edit(bot, chat_id, message_id, text, admin_substitutes_keyboard(subs))
    else:
        safe_edit(bot, chat_id, message_id, "⚙️ <b>تنظیمات ادمین</b>\n\nبه زودی...", admin_back_keyboard())


def _broadcast_preview(data: dict) -> str:
    count = broadcast_service.recipient_count()
    parts = [
        "📢 <b>پیش‌نمایش پیام همگانی</b>",
        "",
        data.get("text", "—"),
        "",
        f"👥 گیرندگان: <b>{count:,}</b>",
    ]
    if data.get("photo_file_id"):
        parts.append("🖼  تصویر: دارد")
    if data.get("button_text"):
        parts.append(f"🔗 دکمه: {data['button_text']}")
    return "\n".join(parts)


def register_admin_handlers(bot: TeleBot) -> None:
    @bot.message_handler(commands=["admin"])
    def handle_admin_command(message: types.Message):
        if not user_service.is_admin(message.from_user.id):
            bot.send_message(message.chat.id, "⛔ دسترسی ندارید.")
            return
        msg = bot.send_message(message.chat.id, "...", parse_mode="HTML")
        show_admin_dashboard(bot, message.chat.id, msg.message_id)

    @bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("admin:"))
    def handle_admin(call: types.CallbackQuery):
        if not user_service.is_admin(call.from_user.id):
            answer_callback(bot, call, "⛔ دسترسی ندارید")
            return

        chat_id = call.message.chat.id
        msg_id = call.message.message_id
        parts = call.data.split(":")
        action = parts[1]

        if action == "main":
            answer_callback(bot, call)
            state_manager.clear(call.from_user.id)
            show_admin_dashboard(bot, chat_id, msg_id)
            return

        if action in ("stats", "popular", "users", "categories", "substitutes", "settings"):
            answer_callback(bot, call)
            show_admin_subpage(bot, chat_id, msg_id, action)
            return

        if action == "recipes":
            answer_callback(bot, call)
            page = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 1
            show_admin_subpage(bot, chat_id, msg_id, "recipes", page)
            return

        if action == "ingredients":
            answer_callback(bot, call)
            page = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 1
            show_admin_subpage(bot, chat_id, msg_id, "ingredients", page)
            return

        if action == "rtog":
            recipe_id = int(parts[2])
            page = int(parts[3]) if len(parts) > 3 else 1
            if len(parts) > 4 and parts[4] == "yes":
                admin_service.toggle_recipe(recipe_id)
                answer_callback(bot, call, "وضعیت غذا تغییر کرد")
                show_admin_subpage(bot, chat_id, msg_id, "recipes", page)
            else:
                answer_callback(bot, call)
                text = build_screen(emoji="⚠️", title="تأیید", description="وضعیت این غذا تغییر کند؟")
                safe_edit(bot, chat_id, msg_id, text, admin_confirm_keyboard(f"admin:rtog:{recipe_id}:{page}:yes", "admin:recipes"))
            return

        if action == "itog":
            ing_id = int(parts[2])
            page = int(parts[3]) if len(parts) > 3 else 1
            if len(parts) > 4 and parts[4] == "yes":
                admin_service.toggle_ingredient(ing_id)
                answer_callback(bot, call, "وضعیت ماده تغییر کرد")
                show_admin_subpage(bot, chat_id, msg_id, "ingredients", page)
            else:
                answer_callback(bot, call)
                text = build_screen(emoji="⚠️", title="تأیید", description="وضعیت این ماده تغییر کند؟")
                safe_edit(bot, chat_id, msg_id, text, admin_confirm_keyboard(f"admin:itog:{ing_id}:{page}:yes", f"admin:ingredients:{page}"))
            return

        if action == "ctog":
            cat_id = int(parts[2])
            if len(parts) > 3 and parts[3] == "yes":
                admin_service.toggle_category(cat_id)
                answer_callback(bot, call, "وضعیت دسته تغییر کرد")
                show_admin_subpage(bot, chat_id, msg_id, "categories")
            else:
                answer_callback(bot, call)
                text = build_screen(emoji="⚠️", title="تأیید", description="وضعیت این دسته تغییر کند؟")
                safe_edit(bot, chat_id, msg_id, text, admin_confirm_keyboard(f"admin:ctog:{cat_id}:yes", "admin:categories"))
            return

        if action == "subdel":
            sub_id = int(parts[2])
            if len(parts) > 3 and parts[3] == "yes":
                admin_service.deactivate_substitute(sub_id)
                answer_callback(bot, call, "جایگزین حذف شد")
                show_admin_subpage(bot, chat_id, msg_id, "substitutes")
            else:
                answer_callback(bot, call)
                text = build_screen(emoji="⚠️", title="تأیید", description="این جایگزین غیرفعال شود؟")
                safe_edit(bot, chat_id, msg_id, text, admin_confirm_keyboard(f"admin:subdel:{sub_id}:yes", "admin:substitutes"))
            return

        if action == "broadcast":
            answer_callback(bot, call)
            state_manager.set_state(call.from_user.id, UserState.WAITING_ADMIN_BROADCAST, chat_id=chat_id, message_id=msg_id)
            text = build_screen(
                emoji="📢",
                title="پیام همگانی",
                description="متن پیام را بنویس و ارسال کن.",
                details=["برای لغو /admin بزن"],
            )
            safe_edit(bot, chat_id, msg_id, text, admin_back_keyboard())
            return

        if action == "bc":
            sub = parts[2]
            st = state_manager.get(call.from_user.id)
            data = dict(st.data)

            if sub == "photo":
                answer_callback(bot, call)
                state_manager.set_state(call.from_user.id, UserState.WAITING_ADMIN_BROADCAST_PHOTO, **data)
                safe_edit(bot, chat_id, msg_id, "🖼 تصویر را بفرست (یا /admin برای لغو)", admin_back_keyboard())
            elif sub == "button":
                answer_callback(bot, call)
                state_manager.set_state(call.from_user.id, UserState.WAITING_ADMIN_BROADCAST_BUTTON, **data)
                safe_edit(bot, chat_id, msg_id, "🔗 دکمه را به صورت «متن|https://url» بنویس:", admin_back_keyboard())
            elif sub == "skip":
                answer_callback(bot, call)
                safe_edit(bot, chat_id, msg_id, _broadcast_preview(data), admin_broadcast_preview_keyboard())
            elif sub == "confirm":
                answer_callback(bot, call, "در حال ارسال...")
                ok, fail = broadcast_service.send(
                    bot,
                    data.get("text", ""),
                    data.get("photo_file_id"),
                    data.get("button_text"),
                    data.get("button_url"),
                )
                state_manager.clear(call.from_user.id)
                text = build_screen(
                    emoji="✅",
                    title="ارسال همگانی",
                    details=[f"موفق: <b>{ok}</b>", f"ناموفق: <b>{fail}</b>"],
                )
                safe_edit(bot, chat_id, msg_id, text, admin_back_keyboard())
            elif sub == "cancel":
                answer_callback(bot, call)
                state_manager.clear(call.from_user.id)
                show_admin_dashboard(bot, chat_id, msg_id)
            return

        answer_callback(bot, call)

    @bot.message_handler(func=lambda m: state_manager.is_waiting(m.from_user.id, UserState.WAITING_ADMIN_BROADCAST))
    def handle_broadcast_text(message: types.Message):
        if not user_service.is_admin(message.from_user.id):
            state_manager.clear(message.from_user.id)
            return
        text = message.text or ""
        st = state_manager.get(message.from_user.id)
        chat_id = st.data.get("chat_id", message.chat.id)
        msg_id = st.data.get("message_id")
        data = {"text": text, "chat_id": chat_id, "message_id": msg_id}
        state_manager.set_state(message.from_user.id, UserState.CONFIRM_ADMIN_BROADCAST, **data)
        preview = _broadcast_preview(data)
        if msg_id:
            safe_edit(message.bot, chat_id, msg_id, preview, admin_broadcast_preview_keyboard())
        else:
            message.bot.send_message(chat_id, preview, reply_markup=admin_broadcast_preview_keyboard(), parse_mode="HTML")

    @bot.message_handler(func=lambda m: state_manager.is_waiting(m.from_user.id, UserState.WAITING_ADMIN_BROADCAST_PHOTO))
    def handle_broadcast_photo(message: types.Message):
        if not user_service.is_admin(message.from_user.id):
            state_manager.clear(message.from_user.id)
            return
        st = state_manager.get(message.from_user.id)
        data = dict(st.data)
        if message.photo:
            data["photo_file_id"] = message.photo[-1].file_id
        state_manager.set_state(message.from_user.id, UserState.CONFIRM_ADMIN_BROADCAST, **data)
        chat_id = data.get("chat_id", message.chat.id)
        msg_id = data.get("message_id")
        preview = _broadcast_preview(data)
        if msg_id:
            safe_edit(message.bot, chat_id, msg_id, preview, admin_broadcast_preview_keyboard())
        else:
            message.bot.send_message(chat_id, preview, reply_markup=admin_broadcast_preview_keyboard(), parse_mode="HTML")

    @bot.message_handler(func=lambda m: state_manager.is_waiting(m.from_user.id, UserState.WAITING_ADMIN_BROADCAST_BUTTON))
    def handle_broadcast_button(message: types.Message):
        if not user_service.is_admin(message.from_user.id):
            state_manager.clear(message.from_user.id)
            return
        raw = (message.text or "").strip()
        st = state_manager.get(message.from_user.id)
        data = dict(st.data)
        if "|" in raw:
            btn_text, btn_url = raw.split("|", 1)
            data["button_text"] = btn_text.strip()
            data["button_url"] = btn_url.strip()
        state_manager.set_state(message.from_user.id, UserState.CONFIRM_ADMIN_BROADCAST, **data)
        chat_id = data.get("chat_id", message.chat.id)
        msg_id = data.get("message_id")
        preview = _broadcast_preview(data)
        if msg_id:
            safe_edit(message.bot, chat_id, msg_id, preview, admin_broadcast_preview_keyboard())
        else:
            message.bot.send_message(chat_id, preview, reply_markup=admin_broadcast_preview_keyboard(), parse_mode="HTML")

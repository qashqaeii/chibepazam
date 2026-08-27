from telebot import TeleBot, types

from bot.handlers.base import safe_edit, answer_callback
from bot.keyboards.panel import panel_home_keyboard, panel_promo_keyboard
from bot.keyboards.main import main_menu_text, main_menu_keyboard
from services.user_service import UserService
from services.promotion_service import PromotionService, DEFAULT_SLOT
from states.user_state import UserState, state_manager
from utils.screen import build_screen, ACTION_FOOTER
from utils.menu_style import section, join_sections


user_service = UserService()
promo_service = PromotionService()


def _deny(bot: TeleBot, chat_id: int) -> None:
    bot.send_message(chat_id, "⛔ این بخش فقط برای مدیر ربات است.", parse_mode="HTML")


def show_panel_home(bot: TeleBot, chat_id: int, message_id: int) -> None:
    promo = promo_service.get_config(DEFAULT_SLOT)
    status = "🟢 فعال" if promo and promo.get("is_active") else "🔴 غیرفعال"
    target = promo.get("link_url", "—") if promo else "—"
    text = build_screen(
        emoji="🛠",
        title="پنل مدیریت",
        description=[
            "مدیریت تبلیغات و تنظیمات ربات «غذا چی بپزم؟»",
            "فقط مدیران به این بخش دسترسی دارند.",
        ],
        details=[
            f"📢  تبلیغ منوی اصلی: <b>{status}</b>",
            f"🔗  لینک فعلی: {target}",
        ],
        footer="👇 گزینه مورد نظر را انتخاب کن",
    )
    safe_edit(bot, chat_id, message_id, text, panel_home_keyboard())


def show_promo_admin(bot: TeleBot, chat_id: int, message_id: int) -> None:
    promo = promo_service.get_config(DEFAULT_SLOT)
    if not promo:
        text = build_screen(
            emoji="📢",
            title="تبلیغات",
            description="رکورد تبلیغ یافت نشد. setup_db را اجرا کن.",
        )
        safe_edit(bot, chat_id, message_id, text, panel_home_keyboard())
        return

    active = "🟢 فعال" if promo.get("is_active") else "🔴 غیرفعال"
    body = join_sections(
        section("وضعیت", [active]),
        section("متن نمایشی در منوی اصلی", [promo.get("body_text") or "—"]),
        section("دکمه", [
            f"🏷  {promo.get('button_label') or '—'}",
            f"🔗  {promo.get('link_url') or '—'}",
        ]),
    )
    text = build_screen(
        emoji="📢",
        title="مدیریت تبلیغ",
        description="تبلیغ در منوی اصلی و دکمه زیر منو نمایش داده می‌شود.",
        body=body,
        footer=ACTION_FOOTER,
    )
    safe_edit(bot, chat_id, message_id, text, panel_promo_keyboard(bool(promo.get("is_active"))))


def register_panel_handlers(bot: TeleBot) -> None:
    @bot.message_handler(commands=["panel"])
    def handle_panel_command(message: types.Message):
        if not user_service.is_admin(message.from_user.id):
            _deny(bot, message.chat.id)
            return
        state_manager.clear(message.from_user.id)
        msg = bot.send_message(message.chat.id, "...", parse_mode="HTML")
        show_panel_home(bot, message.chat.id, msg.message_id)

    @bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("panel:"))
    def handle_panel(call: types.CallbackQuery):
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
            show_panel_home(bot, chat_id, msg_id)
            return

        if action == "promo":
            if len(parts) > 2:
                sub = parts[2]
                if sub == "toggle":
                    active = promo_service.toggle(DEFAULT_SLOT)
                    answer_callback(bot, call, "فعال شد ✅" if active else "غیرفعال شد")
                    show_promo_admin(bot, chat_id, msg_id)
                    return
                if sub == "preview":
                    answer_callback(bot, call)
                    safe_edit(
                        bot, chat_id, msg_id,
                        main_menu_text(greeting="👁 پیش‌نمایش منوی اصلی"),
                        main_menu_keyboard(),
                    )
                    return
                if sub == "edit" and len(parts) > 3:
                    field = parts[3]
                    cfg = promo_service.get_config(DEFAULT_SLOT) or {}
                    state_map = {
                        "text": (UserState.WAITING_PANEL_PROMO_BODY, "متن تبلیغ را بنویس:"),
                        "btn": (UserState.WAITING_PANEL_PROMO_BUTTON, "عنوان دکمه را بنویس:"),
                        "url": (UserState.WAITING_PANEL_PROMO_URL, "لینک را بنویس (@HyperTunnelbot یا https://t.me/...):"),
                    }
                    if field in state_map:
                        st, hint = state_map[field]
                        state_manager.set_state(call.from_user.id, st, chat_id=chat_id, message_id=msg_id)
                        answer_callback(bot, call)
                        safe_edit(
                            bot, chat_id, msg_id,
                            build_screen(emoji="✏️", title="ویرایش تبلیغ", description=hint, footer="برای لغو /panel بزن"),
                            panel_promo_keyboard(bool(cfg.get("is_active"))),
                        )
                    return
            answer_callback(bot, call)
            show_promo_admin(bot, chat_id, msg_id)
            return

        answer_callback(bot, call)

    @bot.message_handler(func=lambda m: state_manager.is_waiting(m.from_user.id, UserState.WAITING_PANEL_PROMO_BODY))
    def handle_promo_body(message: types.Message):
        if not user_service.is_admin(message.from_user.id):
            state_manager.clear(message.from_user.id)
            return
        st = state_manager.get(message.from_user.id)
        state_manager.clear(message.from_user.id)
        text = (message.text or "").strip()
        if len(text) < 5:
            bot.send_message(message.chat.id, "⚠️ متن باید حداقل ۵ حرف باشد.", parse_mode="HTML")
            return
        promo_service.update_body(text)
        msg_id = st.data.get("message_id")
        chat_id = st.data.get("chat_id", message.chat.id)
        if msg_id:
            show_promo_admin(message.bot, chat_id, msg_id)
        bot.send_message(message.chat.id, "✅ متن تبلیغ ذخیره شد.", parse_mode="HTML")

    @bot.message_handler(func=lambda m: state_manager.is_waiting(m.from_user.id, UserState.WAITING_PANEL_PROMO_BUTTON))
    def handle_promo_button(message: types.Message):
        if not user_service.is_admin(message.from_user.id):
            state_manager.clear(message.from_user.id)
            return
        st = state_manager.get(message.from_user.id)
        state_manager.clear(message.from_user.id)
        label = (message.text or "").strip()
        if len(label) < 2:
            bot.send_message(message.chat.id, "⚠️ عنوان دکمه کوتاه است.", parse_mode="HTML")
            return
        promo_service.update_button(label)
        msg_id = st.data.get("message_id")
        chat_id = st.data.get("chat_id", message.chat.id)
        if msg_id:
            show_promo_admin(message.bot, chat_id, msg_id)
        bot.send_message(message.chat.id, "✅ عنوان دکمه ذخیره شد.", parse_mode="HTML")

    @bot.message_handler(func=lambda m: state_manager.is_waiting(m.from_user.id, UserState.WAITING_PANEL_PROMO_URL))
    def handle_promo_url(message: types.Message):
        if not user_service.is_admin(message.from_user.id):
            state_manager.clear(message.from_user.id)
            return
        st = state_manager.get(message.from_user.id)
        state_manager.clear(message.from_user.id)
        raw = (message.text or "").strip()
        try:
            url = promo_service.update_url(raw)
        except ValueError:
            bot.send_message(
                message.chat.id,
                "⚠️ لینک نامعتبر است. مثال: @HyperTunnelbot یا https://t.me/HyperTunnelbot",
                parse_mode="HTML",
            )
            return
        msg_id = st.data.get("message_id")
        chat_id = st.data.get("chat_id", message.chat.id)
        if msg_id:
            show_promo_admin(message.bot, chat_id, msg_id)
        bot.send_message(message.chat.id, f"✅ لینک ذخیره شد:\n{url}", parse_mode="HTML")

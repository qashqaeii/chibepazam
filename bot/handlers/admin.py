from telebot import TeleBot, types

from bot.handlers.base import safe_edit, answer_callback, show_main_menu
from bot.keyboards.admin import admin_dashboard_keyboard, admin_back_keyboard
from services.user_service import UserService
from database.repositories.users import UsersRepository
from database.repositories.ingredients import IngredientsRepository
from database.repositories.recipes import RecipesRepository
from database.repositories.events import EventsRepository
from database.repositories.favorites import FavoritesRepository
from states.user_state import UserState, state_manager


user_service = UserService()
users_repo = UsersRepository()
ingredients_repo = IngredientsRepository()
recipes_repo = RecipesRepository()
events_repo = EventsRepository()
favorites_repo = FavoritesRepository()


from utils.screen import build_screen, list_body, ACTION_FOOTER


def show_admin_dashboard(bot: TeleBot, chat_id: int, message_id: int) -> None:
    users_count = users_repo.count_all()
    active_today = users_repo.count_active_today()
    recipes_count = recipes_repo.count_all()
    ingredients_count = ingredients_repo.count_all()
    searches_today = events_repo.count_searches_today()
    random_today = events_repo.count_today("random")

    text = build_screen(
        emoji="👑",
        title="پنل مدیریت",
        description="خلاصه وضعیت ربات «غذا چی بپزم؟»",
        details=[
            f"📊  کاربران: <b>{users_count:,}</b>",
            f"🟢  فعال امروز: <b>{active_today:,}</b>",
            f"🍲  غذاها: <b>{recipes_count:,}</b>",
            f"🥕  مواد اولیه: <b>{ingredients_count:,}</b>",
            f"🔎  جستجوی امروز: <b>{searches_today:,}</b>",
            f"🎲  پیشنهاد شانسی امروز: <b>{random_today:,}</b>",
        ],
        footer=ACTION_FOOTER,
    )
    safe_edit(bot, chat_id, message_id, text, admin_dashboard_keyboard())


def show_admin_subpage(bot: TeleBot, chat_id: int, message_id: int, action: str) -> None:
    if action == "stats":
        text = (
            "📊 <b>آمار ربات</b>\n\n"
            f"👥 کل کاربران: {users_repo.count_all():,}\n"
            f"🟢 فعال امروز: {users_repo.count_active_today():,}\n"
            f"🔎 جستجو امروز: {events_repo.count_searches_today():,}\n"
            f"🎲 Random امروز: {events_repo.count_today('random'):,}"
        )
        safe_edit(bot, chat_id, message_id, text, admin_back_keyboard())
    elif action == "popular":
        popular = favorites_repo.count_popular(10)
        lines = "هنوز داده‌ای نیست." if not popular else "\n".join(
            f"{i+1}. {p.get('emoji', '🍲')} {p['name']} — {p['fav_count']} ❤️"
            for i, p in enumerate(popular)
        )
        safe_edit(bot, chat_id, message_id, f"❤️ <b>محبوب‌ترین غذاها</b>\n\n{lines}", admin_back_keyboard())
    elif action == "users":
        text = (
            "👥 <b>کاربران</b>\n\n"
            f"تعداد کل: {users_repo.count_all():,}\n"
            f"فعال امروز: {users_repo.count_active_today():,}"
        )
        safe_edit(bot, chat_id, message_id, text, admin_back_keyboard())
    elif action == "recipes":
        recipes = recipes_repo.get_all_active()
        lines = "\n".join(f"{'✅' if r['is_active'] else '❌'} {r['emoji']} {r['name']}" for r in recipes[:20])
        text = f"🍲 <b>مدیریت غذاها</b> ({len(recipes)})\n\n{lines or '—'}"
        safe_edit(bot, chat_id, message_id, text, admin_back_keyboard())
    elif action == "ingredients":
        text = f"🥕 <b>مواد اولیه</b>\n\nتعداد: {ingredients_repo.count_all():,}"
        safe_edit(bot, chat_id, message_id, text, admin_back_keyboard())
    elif action == "categories":
        cats = ingredients_repo.get_categories()
        lines = "\n".join(f"{c['emoji']} {c['name']}" for c in cats)
        safe_edit(bot, chat_id, message_id, f"📂 <b>دسته‌بندی‌ها</b>\n\n{lines}", admin_back_keyboard())
    else:
        safe_edit(bot, chat_id, message_id, "⚙️ <b>تنظیمات ادمین</b>\n\nبه زودی...", admin_back_keyboard())


def register_admin_handlers(bot: TeleBot) -> None:
    @bot.message_handler(commands=["admin"])
    def handle_admin_command(message: types.Message):
        if not user_service.is_admin(message.from_user.id):
            bot.send_message(message.chat.id, "⛔ دسترسی ندارید.")
            return
        bot.send_message(
            message.chat.id,
            "👑 در حال بارگذاری پنل...",
            parse_mode="HTML",
        )
        msg = bot.send_message(message.chat.id, "...", parse_mode="HTML")
        show_admin_dashboard(bot, message.chat.id, msg.message_id)

    @bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("admin:"))
    def handle_admin(call: types.CallbackQuery):
        if not user_service.is_admin(call.from_user.id):
            answer_callback(bot, call, "⛔ دسترسی ندارید")
            return

        answer_callback(bot, call)
        chat_id = call.message.chat.id
        msg_id = call.message.message_id
        action = call.data.split(":")[1]

        if action == "main":
            show_admin_dashboard(bot, chat_id, msg_id)

        elif action == "stats":
            show_admin_subpage(bot, chat_id, msg_id, "stats")

        elif action == "popular":
            show_admin_subpage(bot, chat_id, msg_id, "popular")

        elif action == "users":
            show_admin_subpage(bot, chat_id, msg_id, "users")

        elif action == "recipes":
            show_admin_subpage(bot, chat_id, msg_id, "recipes")

        elif action == "ingredients":
            show_admin_subpage(bot, chat_id, msg_id, "ingredients")

        elif action == "categories":
            show_admin_subpage(bot, chat_id, msg_id, "categories")

        elif action == "broadcast":
            state_manager.set_state(call.from_user.id, UserState.WAITING_ADMIN_BROADCAST)
            text = "📢 پیام همگانی رو بنویس:\n\n(برای لغو /admin بزن)"
            safe_edit(bot, chat_id, msg_id, text, admin_back_keyboard())

        elif action == "settings":
            show_admin_subpage(bot, chat_id, msg_id, "settings")

    @bot.message_handler(func=lambda m: state_manager.is_waiting(m.from_user.id, UserState.WAITING_ADMIN_BROADCAST))
    def handle_broadcast(message: types.Message):
        if not user_service.is_admin(message.from_user.id):
            state_manager.clear(message.from_user.id)
            return
        state_manager.clear(message.from_user.id)
        bot.send_message(message.chat.id, "📢 ارسال همگانی در نسخه بعدی فعال می‌شود.", parse_mode="HTML")

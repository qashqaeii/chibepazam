from telebot import types

from bot.keyboards.navigation import nav_row


def admin_dashboard_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("🍲 مدیریت غذاها", callback_data="admin:recipes"),
        types.InlineKeyboardButton("🥕 مواد اولیه", callback_data="admin:ingredients"),
    )
    kb.add(
        types.InlineKeyboardButton("📂 دسته‌بندی‌ها", callback_data="admin:categories"),
        types.InlineKeyboardButton("👥 کاربران", callback_data="admin:users"),
    )
    kb.add(
        types.InlineKeyboardButton("📊 آمار ربات", callback_data="admin:stats"),
        types.InlineKeyboardButton("❤️ محبوب‌ترین‌ها", callback_data="admin:popular"),
    )
    kb.add(
        types.InlineKeyboardButton("📢 ارسال همگانی", callback_data="admin:broadcast"),
        types.InlineKeyboardButton("⚙️ تنظیمات", callback_data="admin:settings"),
    )
    kb.add(types.InlineKeyboardButton("🏠 خروج از مدیریت", callback_data="nav:home"))
    return kb


def admin_back_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.row(
        types.InlineKeyboardButton("⬅️ بازگشت", callback_data="admin:main"),
        types.InlineKeyboardButton("🏠 پنل مدیریت", callback_data="admin:main"),
    )
    return kb

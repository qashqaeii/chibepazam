from telebot import types

from bot.keyboards.builder import btn, append_nav


def admin_dashboard_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        btn("🍲  غذاها", "admin:recipes"),
        btn("🥕  مواد", "admin:ingredients"),
    )
    kb.add(
        btn("📂  دسته‌ها", "admin:categories"),
        btn("👥  کاربران", "admin:users"),
    )
    kb.add(
        btn("📊  آمار", "admin:stats"),
        btn("❤️  محبوب‌ها", "admin:popular"),
    )
    kb.add(
        btn("📢  همگانی", "admin:broadcast"),
        btn("⚙️  تنظیمات", "admin:settings"),
    )
    kb.add(btn("🏠  خروج", "nav:home"))
    return kb


def admin_back_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.row(
        btn("⬅️  بازگشت", "admin:main"),
        btn("🏠  پنل", "admin:main"),
    )
    return kb

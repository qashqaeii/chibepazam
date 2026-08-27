from telebot import types

from bot.keyboards.navigation import nav_row


def main_menu_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(types.InlineKeyboardButton("🧺 با مواد خونه چی بپزم؟", callback_data="menu:pantry"))
    kb.add(
        types.InlineKeyboardButton("🎲 پیشنهاد شانسی", callback_data="menu:random"),
        types.InlineKeyboardButton("🔍 جستجوی غذا", callback_data="menu:search"),
    )
    kb.add(
        types.InlineKeyboardButton("❤️ علاقه‌مندی‌ها", callback_data="menu:favorites"),
        types.InlineKeyboardButton("🕘 تاریخچه", callback_data="menu:history"),
    )
    kb.add(
        types.InlineKeyboardButton("👤 حساب من", callback_data="menu:profile"),
        types.InlineKeyboardButton("⚙️ تنظیمات", callback_data="menu:settings"),
    )
    return kb


MAIN_MENU_TEXT = (
    "🍲 <b>غذا چی بپزم؟</b>\n\n"
    "امروز چی درست کنیم؟ 😋\n\n"
    "مواد غذایی که توی خونه داری رو انتخاب کن\n"
    "تا بهترین غذاها رو بهت پیشنهاد بدم.\n\n"
    "👇 یکی از گزینه‌ها رو انتخاب کن"
)


def profile_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(*nav_row())
    return kb

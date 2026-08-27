from telebot import types

from bot.keyboards.builder import btn, append_nav
from bot.keyboards.navigation import nav_row


def main_menu_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(btn("🧺  با مواد خونه چی بپزم؟", "menu:pantry"))
    kb.add(
        btn("🎲  پیشنهاد شانسی", "menu:random"),
        btn("🔍  جستجوی غذا", "menu:search"),
    )
    kb.add(
        btn("❤️  علاقه‌مندی‌ها", "menu:favorites"),
        btn("🕘  تاریخچه", "menu:history"),
    )
    kb.add(
        btn("👤  حساب من", "menu:profile"),
        btn("⚙️  تنظیمات", "menu:settings"),
    )
    return kb


def main_menu_text(greeting: str | None = None) -> str:
    from utils.screen import build_screen, SEPARATOR

    base = build_screen(
        emoji="🍲",
        title="غذا چی بپزم؟",
        description=[
            "امروز چی درست کنیم؟ 😋",
            "مواد خونه‌ات رو انتخاب کن تا بهترین غذا رو پیشنهاد بدم.",
        ],
        details=[
            "🧺  انتخاب مواد موجود",
            "🔥  پیشنهاد هوشمند",
            "🎲  یا یک غذای شانسی!",
        ],
        footer="👇 یکی از گزینه‌ها رو انتخاب کن",
    )
    if greeting:
        return f"{greeting}\n\n{base}"
    return base


# Backward compat
MAIN_MENU_TEXT = main_menu_text()


def profile_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    return append_nav(kb)

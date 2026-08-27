from telebot import types

from bot.keyboards.builder import btn, append_nav


def main_menu_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    # ── پیشنهاد غذا
    kb.add(btn("🧺  با مواد خونه", "menu:pantry"))
    kb.add(btn("🤔  نمی‌دونم چی می‌خوام", "menu:decide"))
    kb.add(
        btn("🎲  پیشنهاد شانسی", "menu:random"),
        btn("🔍  جستجوی غذا", "menu:search"),
    )
    # ── لیست‌ها
    kb.add(
        btn("🛒  لیست خرید", "shop:cart"),
        btn("❤️  علاقه‌مندی‌ها", "menu:favorites"),
    )
    kb.add(
        btn("🕘  تاریخچه", "menu:history"),
        btn("👤  حساب من", "menu:profile"),
    )
    kb.add(btn("⚙️  تنظیمات", "menu:settings"))
    return kb


def main_menu_text(greeting: str | None = None) -> str:
    from utils.screen import build_screen, SEPARATOR
    from utils.menu_style import section, join_sections, status_chip

    intro = build_screen(
        emoji="🍲",
        title="غذا چی بپزم؟",
        description=[
            "دستیار آشپزی هوشمند برای انتخاب غذای روزانه 🍽",
            "مواد خونه‌ات را بگو — بهترین پیشنهاد را می‌دهم.",
        ],
        footer=None,
    )
    guide = join_sections(
        section("چطور شروع کنم؟", [
            "مواد موجود را از «با مواد خونه» انتخاب کن",
            "فیلتر بزن و «چی می‌تونم بپزم» را بزن",
            "یا از «نمی‌دونم چی می‌خوام» راهنمایی بگیر",
        ]),
        section("امکانات", [
            "🎲 پیشنهاد شانسی با فیلتر",
            "🔍 جستجو در نام غذا و مواد",
            "🛒 لیست خرید ترکیبی چند غذا",
            "⭐ امتیاز، پخت و اشتراک غذا",
        ]),
    )
    footer = "👇 از منوی زیر گزینه مورد نظر را انتخاب کن"
    base = f"{intro}\n{guide}\n\n{footer}"
    if greeting:
        return f"{greeting}\n\n{base}"
    return base


MAIN_MENU_TEXT = main_menu_text()


def profile_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        btn("🧺  مواد خونه", "menu:pantry"),
        btn("❤️  علاقه‌مندی‌ها", "menu:favorites"),
    )
    kb.add(btn("⚙️  تنظیمات", "menu:settings"))
    return append_nav(kb)

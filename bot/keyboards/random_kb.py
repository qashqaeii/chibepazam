from telebot import types

from bot.keyboards.builder import btn, append_nav


def random_menu_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(btn("🎲  کاملاً شانسی", "random:full"))
    kb.row(
        btn("⚡  زیر ۱ ساعت", "random:fast"),
        btn("💰  اقتصادی", "random:cheap"),
    )
    kb.row(
        btn("🍗  با مرغ", "random:chicken"),
        btn("🥩  گوشتی", "random:meat"),
    )
    kb.row(
        btn("🌱  گیاهی", "random:vegetarian"),
        btn("🍚  برنجی", "random:rice"),
    )
    kb.row(
        btn("🥖  نونی", "random:bread"),
        btn("🥘  سنتی", "random:traditional"),
    )
    return append_nav(kb)


def random_result_keyboard(recipe_id: int) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.row(
        btn("📖  مشاهده غذا", f"recipe:view:{recipe_id}"),
        btn("🎲  یکی دیگه", "random:next"),
    )
    kb.row(
        btn("❤️  ذخیره", f"recipe:favorite:{recipe_id}"),
        btn("🔍  جستجو", "menu:search"),
    )
    kb.add(btn("🏠  صفحه اصلی", "nav:home"))
    return kb


def search_prompt_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(btn("💡  مثال: قورمه سبزی", "noop"))
    return append_nav(kb)

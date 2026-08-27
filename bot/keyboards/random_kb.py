from telebot import types

from bot.keyboards.builder import btn, append_nav


def random_menu_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(btn("🎲  کاملاً شانسی", "random:full"))
    kb.add(
        btn("⚡  سریع", "random:fast"),
        btn("💰  اقتصادی", "random:cheap"),
    )
    kb.add(
        btn("🍗  با مرغ", "random:chicken"),
        btn("🥩  گوشتی", "random:meat"),
    )
    kb.add(
        btn("🌱  بدون گوشت", "random:vegetarian"),
        btn("🍚  برنجی", "random:rice"),
    )
    kb.add(
        btn("🥖  نونی", "random:bread"),
        btn("🥘  سنتی", "random:traditional"),
    )
    return append_nav(kb)


def random_result_keyboard(recipe_id: int) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        btn("📖  مشاهده غذا", f"recipe:view:{recipe_id}"),
        btn("🎲  یکی دیگه", "random:next"),
    )
    kb.add(
        btn("❤️  ذخیره", f"recipe:favorite:{recipe_id}"),
        btn("🏠  خانه", "nav:home"),
    )
    return kb


def search_prompt_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    return append_nav(kb)

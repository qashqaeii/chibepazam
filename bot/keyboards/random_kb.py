from telebot import types

from bot.keyboards.navigation import nav_row


def random_menu_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(types.InlineKeyboardButton("🎲 کاملاً شانسی", callback_data="random:full"))
    kb.add(
        types.InlineKeyboardButton("⚡ سریع", callback_data="random:fast"),
        types.InlineKeyboardButton("💰 اقتصادی", callback_data="random:cheap"),
    )
    kb.add(
        types.InlineKeyboardButton("🍗 با مرغ", callback_data="random:chicken"),
        types.InlineKeyboardButton("🥩 گوشتی", callback_data="random:meat"),
    )
    kb.add(
        types.InlineKeyboardButton("🌱 بدون گوشت", callback_data="random:vegetarian"),
        types.InlineKeyboardButton("🍚 برنجی", callback_data="random:rice"),
    )
    kb.add(
        types.InlineKeyboardButton("🥖 نونی", callback_data="random:bread"),
        types.InlineKeyboardButton("🥘 سنتی", callback_data="random:traditional"),
    )
    kb.row(*nav_row())
    return kb


def random_result_keyboard(recipe_id: int) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("📖 ببینمش", callback_data=f"recipe:view:{recipe_id}"),
        types.InlineKeyboardButton("🎲 یکی دیگه", callback_data="random:next"),
    )
    kb.add(
        types.InlineKeyboardButton("❤️ ذخیره", callback_data=f"recipe:favorite:{recipe_id}"),
        types.InlineKeyboardButton("🏠 خانه", callback_data="nav:home"),
    )
    return kb


def search_prompt_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.row(*nav_row())
    return kb

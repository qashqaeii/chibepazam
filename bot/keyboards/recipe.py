from telebot import types

from bot.keyboards.navigation import nav_row, pagination_row


def recipe_detail_keyboard(recipe_id: int, is_favorite: bool) -> types.InlineKeyboardMarkup:
    fav_text = "💔 حذف از علاقه‌مندی" if is_favorite else "❤️ ذخیره"
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("🥕 مواد لازم", callback_data=f"recipe:ingredients:{recipe_id}"),
        types.InlineKeyboardButton("👨‍🍳 دستور پخت", callback_data=f"recipe:steps:{recipe_id}"),
    )
    kb.add(
        types.InlineKeyboardButton("🛒 چیزایی که ندارم", callback_data=f"recipe:missing:{recipe_id}"),
        types.InlineKeyboardButton(fav_text, callback_data=f"recipe:favorite:{recipe_id}"),
    )
    kb.add(
        types.InlineKeyboardButton("🔄 غذای مشابه", callback_data=f"recipe:similar:{recipe_id}"),
        types.InlineKeyboardButton("📤 اشتراک", callback_data=f"recipe:share:{recipe_id}"),
    )
    kb.row(*nav_row())
    return kb


def recipe_list_keyboard(recipes: list[dict], prefix: str = "recipe:view") -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=1)
    for r in recipes:
        kb.add(
            types.InlineKeyboardButton(
                f"{r.get('emoji', '🍲')} {r['name']}",
                callback_data=f"{prefix}:{r['id']}",
            )
        )
    kb.row(*nav_row())
    return kb


def recommend_list_keyboard(items: list[dict]) -> types.InlineKeyboardMarkup:
    from utils.telegram import match_emoji

    kb = types.InlineKeyboardMarkup(row_width=1)
    for item in items:
        recipe = item["recipe"]
        score = item["score"]
        emoji = match_emoji(score)
        kb.add(
            types.InlineKeyboardButton(
                f"{emoji} {recipe['name']} — {score:.0f}٪",
                callback_data=f"recipe:view:{recipe['id']}",
            )
        )
    return kb


def favorites_keyboard(recipes: list[dict], page: int, total_pages: int) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=1)
    for r in recipes:
        kb.add(
            types.InlineKeyboardButton(
                f"{r.get('emoji', '🍲')} {r['name']}",
                callback_data=f"recipe:view:{r['id']}",
            )
        )
    pag = pagination_row("fav", page, total_pages)
    if pag:
        kb.row(*pag)
    kb.row(*nav_row())
    return kb

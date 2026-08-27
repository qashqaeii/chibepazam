from telebot import types

from bot.keyboards.builder import btn, append_nav, append_pagination
from bot.keyboards.navigation import nav_row


def recipe_detail_keyboard(recipe_id: int, is_favorite: bool) -> types.InlineKeyboardMarkup:
    fav_text = "💔  حذف علاقه‌مندی" if is_favorite else "❤️  ذخیره"
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        btn("🥕  مواد لازم", f"recipe:ingredients:{recipe_id}"),
        btn("👨‍🍳  دستور پخت", f"recipe:steps:{recipe_id}"),
    )
    kb.add(
        btn("🛒  ندارم", f"recipe:missing:{recipe_id}"),
        btn(fav_text, f"recipe:favorite:{recipe_id}"),
    )
    kb.add(
        btn("🔄  مشابه", f"recipe:similar:{recipe_id}"),
        btn("📤  اشتراک", f"recipe:share:{recipe_id}"),
    )
    return append_nav(kb)


def recipe_sub_keyboard(recipe_id: int) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(btn("⬅️  بازگشت به غذا", f"recipe:view:{recipe_id}:b"))
    kb.add(btn("🏠  خانه", "nav:home"))
    return kb


def recipe_list_keyboard(recipes: list[dict], prefix: str = "recipe:view") -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=1)
    for r in recipes:
        kb.add(btn(f"{r.get('emoji', '🍲')}  {r['name']}", f"{prefix}:{r['id']}"))
    return append_nav(kb)


def recommend_list_keyboard(items: list[dict]) -> types.InlineKeyboardMarkup:
    from utils.telegram import match_emoji

    kb = types.InlineKeyboardMarkup(row_width=1)
    for item in items:
        recipe = item["recipe"]
        score = item["score"]
        emoji = match_emoji(score)
        kb.add(
            btn(
                f"{emoji}  {recipe['name']}  —  {score:.0f}٪",
                f"recipe:view:{recipe['id']}",
            )
        )
    return kb


def favorites_keyboard(recipes: list[dict], page: int, total_pages: int) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=1)
    for r in recipes:
        kb.add(btn(f"{r.get('emoji', '🍲')}  {r['name']}", f"recipe:view:{r['id']}"))
    append_pagination(kb, "fav", page, total_pages)
    return append_nav(kb)

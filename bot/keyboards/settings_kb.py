from telebot import types

from bot.keyboards.builder import btn, append_nav, append_pagination
from config import Config


def settings_keyboard(notifications: bool) -> types.InlineKeyboardMarkup:
    notif_text = "🔔  اعلان: روشن" if notifications else "🔕  اعلان: خاموش"
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(btn("🏠  مواد همیشگی", "settings:permanent"))
    kb.add(
        btn("👨‍👩‍👧  تعداد نفرات", "settings:servings"),
        btn("🌱  رژیم غذایی", "settings:diet"),
    )
    kb.add(btn("🚫  مواد غیرمجاز", "settings:forbidden"))
    kb.add(btn(notif_text, "settings:notifications"))
    return append_nav(kb)


def servings_keyboard(current: int) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=3)
    for n in [1, 2, 3, 4, 5, 6]:
        mark = "✅ " if n == current else ""
        kb.add(btn(f"{mark}{n} نفر", f"settings:servings:{n}"))
    return append_nav(kb, back="menu:settings")


def diet_keyboard(current: str) -> types.InlineKeyboardMarkup:
    options = [
        ("none", "🍽  بدون محدودیت"),
        ("vegetarian", "🌱  گیاهخواری"),
        ("vegan", "🥬  وگان"),
    ]
    kb = types.InlineKeyboardMarkup(row_width=1)
    for key, label in options:
        mark = "✅ " if key == current else ""
        kb.add(btn(f"{mark}{label}", f"settings:diet:{key}"))
    return append_nav(kb, back="menu:settings")


def permanent_keyboard(ingredients: list[dict], selected_ids: set[int], page: int, total_pages: int) -> types.InlineKeyboardMarkup:
    from utils.pagination import paginate

    page_items, current_page, total_pages = paginate(ingredients, page, Config.INGREDIENTS_PER_PAGE)
    kb = types.InlineKeyboardMarkup(row_width=2)
    for i in range(0, len(page_items), 2):
        row = []
        for ing in page_items[i : i + 2]:
            mark = "✅" if ing["id"] in selected_ids else "⬜"
            row.append(
                btn(
                    f"{mark} {ing['emoji']} {ing['name']}",
                    f"settings:perm:{ing['id']}:{current_page}",
                )
            )
        kb.row(*row)
    append_pagination(kb, "perm", current_page, total_pages)
    return append_nav(kb, back="menu:settings")

from telebot import types

from bot.keyboards.navigation import nav_row


def settings_keyboard(notifications: bool) -> types.InlineKeyboardMarkup:
    notif_text = "🔔 اعلان‌ها: روشن" if notifications else "🔔 اعلان‌ها: خاموش"
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton("🏠 مواد همیشگی من", callback_data="settings:permanent"))
    kb.add(
        types.InlineKeyboardButton("👨‍👩‍👧 تعداد نفرات", callback_data="settings:servings"),
        types.InlineKeyboardButton("🌱 رژیم غذایی", callback_data="settings:diet"),
    )
    kb.add(types.InlineKeyboardButton("🚫 مواد غیرمجاز", callback_data="settings:forbidden"))
    kb.add(types.InlineKeyboardButton(notif_text, callback_data="settings:notifications"))
    kb.row(*nav_row())
    return kb


def servings_keyboard(current: int) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=3)
    for n in [1, 2, 3, 4, 5, 6]:
        mark = "✅ " if n == current else ""
        kb.add(types.InlineKeyboardButton(f"{mark}{n} نفر", callback_data=f"settings:servings:{n}"))
    kb.row(*nav_row(back_callback="menu:settings"))
    return kb


def diet_keyboard(current: str) -> types.InlineKeyboardMarkup:
    options = [
        ("none", "🍽 بدون محدودیت"),
        ("vegetarian", "🌱 گیاهخواری"),
        ("vegan", "🥬 وگان"),
    ]
    kb = types.InlineKeyboardMarkup(row_width=1)
    for key, label in options:
        mark = "✅ " if key == current else ""
        kb.add(types.InlineKeyboardButton(f"{mark}{label}", callback_data=f"settings:diet:{key}"))
    kb.row(*nav_row(back_callback="menu:settings"))
    return kb


def permanent_keyboard(ingredients: list[dict], selected_ids: set[int], page: int, total_pages: int) -> types.InlineKeyboardMarkup:
    from bot.keyboards.navigation import pagination_row
    from utils.pagination import paginate
    from config import Config

    page_items, current_page, total_pages = paginate(ingredients, page, Config.INGREDIENTS_PER_PAGE)
    kb = types.InlineKeyboardMarkup(row_width=2)
    for i in range(0, len(page_items), 2):
        row = []
        for ing in page_items[i : i + 2]:
            mark = "✅" if ing["id"] in selected_ids else "⬜"
            row.append(
                types.InlineKeyboardButton(
                    f"{mark} {ing['emoji']} {ing['name']}",
                    callback_data=f"settings:perm:{ing['id']}:{current_page}",
                )
            )
        kb.row(*row)
    pag = pagination_row("perm", current_page, total_pages)
    if pag:
        kb.row(*pag)
    kb.row(*nav_row(back_callback="menu:settings"))
    return kb

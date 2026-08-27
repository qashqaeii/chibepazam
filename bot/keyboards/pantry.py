from telebot import types

from bot.keyboards.navigation import nav_row, pagination_row
from config import Config


def pantry_main_keyboard(categories: list[dict], selected_count: int) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    for i in range(0, len(categories), 2):
        row = []
        for cat in categories[i : i + 2]:
            row.append(
                types.InlineKeyboardButton(
                    f"{cat['emoji']} {cat['name']}",
                    callback_data=f"pantry:category:{cat['id']}",
                )
            )
        kb.row(*row)

    kb.add(types.InlineKeyboardButton("📋 انتخاب‌های من", callback_data="pantry:selected"))
    kb.add(types.InlineKeyboardButton("🔥 چی می‌تونم بپزم؟", callback_data="pantry:recommend"))
    kb.row(*nav_row())
    return kb


def pantry_category_keyboard(
    category: dict,
    ingredients: list[dict],
    selected_ids: set[int],
    page: int = 1,
) -> types.InlineKeyboardMarkup:
    from utils.pagination import paginate

    page_items, current_page, total_pages = paginate(ingredients, page, Config.INGREDIENTS_PER_PAGE)
    kb = types.InlineKeyboardMarkup(row_width=2)

    for i in range(0, len(page_items), 2):
        row = []
        for ing in page_items[i : i + 2]:
            mark = "✅" if ing["id"] in selected_ids else "⬜"
            row.append(
                types.InlineKeyboardButton(
                    f"{mark} {ing['emoji']} {ing['name']}",
                    callback_data=f"pantry:ingredient:{ing['id']}:{category['id']}:{current_page}",
                )
            )
        kb.row(*row)

    pag = pagination_row(f"ing:{category['id']}", current_page, total_pages)
    if pag:
        kb.row(*pag)

    kb.add(types.InlineKeyboardButton("✅ تمام", callback_data=f"pantry:done:{category['id']}"))
    kb.row(*nav_row(back_callback="pantry:main"))
    return kb


def pantry_selected_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton("🔥 پیشنهاد غذا", callback_data="pantry:recommend"))
    kb.add(
        types.InlineKeyboardButton("➕ افزودن مواد", callback_data="pantry:main"),
        types.InlineKeyboardButton("🗑 پاک کردن همه", callback_data="pantry:clear"),
    )
    kb.row(*nav_row(back_callback="pantry:main"))
    return kb


def pantry_clear_confirm_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton("✅ بله، پاک کن", callback_data="pantry:clear:yes"))
    kb.add(types.InlineKeyboardButton("❌ انصراف", callback_data="pantry:selected"))
    return kb


def recommend_keyboard(page: int, total_pages: int) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=1)
    if page < total_pages:
        kb.add(types.InlineKeyboardButton("➡️ پیشنهادهای بیشتر", callback_data=f"page:rec:{page + 1}"))
    kb.add(types.InlineKeyboardButton("🎲 یکی رو خودت انتخاب کن", callback_data="menu:random"))
    kb.row(
        types.InlineKeyboardButton("⬅️ تغییر مواد", callback_data="pantry:main"),
        types.InlineKeyboardButton("🏠 خانه", callback_data="nav:home"),
    )
    return kb

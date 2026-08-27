from telebot import types

from bot.keyboards.builder import btn, append_nav, append_pagination
from bot.keyboards.navigation import nav_row
from config import Config


def pantry_main_keyboard(categories: list[dict], selected_count: int) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    for i in range(0, len(categories), 2):
        row = []
        for cat in categories[i : i + 2]:
            row.append(btn(f"{cat['emoji']}  {cat['name']}", f"pantry:category:{cat['id']}"))
        kb.row(*row)

    kb.add(btn("📋  انتخاب‌های من", "pantry:selected"))
    kb.add(btn("🔥  چی می‌تونم بپزم؟", "pantry:recommend"))
    return append_nav(kb)


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
                btn(
                    f"{mark} {ing['emoji']} {ing['name']}",
                    f"pantry:ingredient:{ing['id']}:{category['id']}:{current_page}",
                )
            )
        kb.row(*row)

    append_pagination(kb, f"ing:{category['id']}", current_page, total_pages)
    kb.add(btn("✅  تأیید و بازگشت", f"pantry:done:{category['id']}"))
    return append_nav(kb, back="pantry:main")


def pantry_selected_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(btn("🔥  پیشنهاد غذا", "pantry:recommend"))
    kb.add(
        btn("➕  افزودن مواد", "pantry:main"),
        btn("🗑  پاک کردن همه", "pantry:clear"),
    )
    return append_nav(kb, back="pantry:main")


def pantry_clear_confirm_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(btn("✅  بله، پاک کن", "pantry:clear:yes"))
    kb.add(btn("❌  انصراف", "pantry:selected"))
    return kb


def recommend_keyboard(page: int, total_pages: int) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    if page < total_pages:
        kb.add(btn("➡️  پیشنهادهای بیشتر", f"page:rec:{page + 1}"))
    kb.add(btn("🎲  پیشنهاد شانسی", "menu:random"))
    kb.row(
        btn("⬅️  تغییر مواد", "pantry:main"),
        btn("🏠  خانه", "nav:home"),
    )
    return kb

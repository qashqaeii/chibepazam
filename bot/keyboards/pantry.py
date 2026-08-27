from telebot import types

from bot.keyboards.builder import btn, append_nav, append_pagination
from config import Config

FILTER_KEYS = {
    "time": ("time_short", "time_medium"),
    "cost": ("cost_low", "cost_high"),
    "meal": ("meal_polo", "meal_stew", "meal_kebab", "meal_ash"),
    "diet": ("veg_only", "vegan_only"),
    "extra": ("available_now", "one_missing"),
}

FILTER_LABELS = {
    "time_short": "⚡ زیر ۱ ساعت",
    "time_medium": "⏳ تا ۲ ساعت",
    "cost_low": "💚 اقتصادی",
    "cost_high": "💎 گران‌تر",
    "meal_polo": "🍚 پلو",
    "meal_stew": "🥘 خورش",
    "meal_kebab": "🍖 کباب",
    "meal_ash": "🥣 آش",
    "veg_only": "🌱 گیاهی",
    "vegan_only": "🥬 وگان",
    "available_now": "✅ همین الان",
    "one_missing": "۱ ماده کم",
}


def _mark(active: set[str], key: str) -> str:
    return "✅" if key in active else "⬜"


def pantry_main_keyboard(categories: list[dict], selected_count: int) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    for i in range(0, len(categories), 2):
        row = []
        for cat in categories[i : i + 2]:
            row.append(btn(f"{cat['emoji']}  {cat['name']}", f"pantry:category:{cat['id']}"))
        kb.row(*row)

    kb.add(btn("📋  مواد انتخاب‌شده", "pantry:selected"))
    kb.add(
        btn("🎛  فیلتر پیشنهاد", "pantry:recommend"),
        btn("🔥  چی می‌تونم بپزم؟", "pantry:recgo"),
    )
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
    kb.add(
        btn("🎛  فیلتر", "pantry:recommend"),
        btn("🔥  پیشنهاد غذا", "pantry:recgo"),
    )
    kb.add(
        btn("➕  افزودن مواد", "pantry:main"),
        btn("🗑  پاک کردن", "pantry:clear"),
    )
    return append_nav(kb, back="pantry:main")


def pantry_clear_confirm_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.row(btn("✅  بله، پاک کن", "pantry:clear:yes"), btn("❌  انصراف", "pantry:selected"))
    return kb


def recommend_filters_keyboard(active: set[str]) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.row(
        btn(f"{_mark(active, 'time_short')} {FILTER_LABELS['time_short']}", "pantry:flt:time_short"),
        btn(f"{_mark(active, 'time_medium')} {FILTER_LABELS['time_medium']}", "pantry:flt:time_medium"),
    )
    kb.row(
        btn(f"{_mark(active, 'cost_low')} {FILTER_LABELS['cost_low']}", "pantry:flt:cost_low"),
        btn(f"{_mark(active, 'cost_high')} {FILTER_LABELS['cost_high']}", "pantry:flt:cost_high"),
    )
    kb.row(
        btn(f"{_mark(active, 'meal_polo')} {FILTER_LABELS['meal_polo']}", "pantry:flt:meal_polo"),
        btn(f"{_mark(active, 'meal_stew')} {FILTER_LABELS['meal_stew']}", "pantry:flt:meal_stew"),
    )
    kb.row(
        btn(f"{_mark(active, 'meal_kebab')} {FILTER_LABELS['meal_kebab']}", "pantry:flt:meal_kebab"),
        btn(f"{_mark(active, 'meal_ash')} {FILTER_LABELS['meal_ash']}", "pantry:flt:meal_ash"),
    )
    kb.row(
        btn(f"{_mark(active, 'veg_only')} {FILTER_LABELS['veg_only']}", "pantry:flt:veg_only"),
        btn(f"{_mark(active, 'vegan_only')} {FILTER_LABELS['vegan_only']}", "pantry:flt:vegan_only"),
    )
    kb.row(
        btn(f"{_mark(active, 'available_now')} {FILTER_LABELS['available_now']}", "pantry:flt:available_now"),
        btn(f"{_mark(active, 'one_missing')} {FILTER_LABELS['one_missing']}", "pantry:flt:one_missing"),
    )
    kb.add(btn("🔥  نمایش نتایج", "pantry:recgo"))
    kb.add(btn("🗑  پاک کردن فیلترها", "pantry:fltclr"))
    return append_nav(kb, back="pantry:main")


def recommend_keyboard(page: int, total_pages: int) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    if page < total_pages:
        kb.add(btn("➡️  صفحه بعد", f"page:rec:{page + 1}"))
    kb.row(
        btn("🎛  تغییر فیلتر", "pantry:recommend"),
        btn("🧺  تغییر مواد", "pantry:main"),
    )
    kb.add(btn("🎲  پیشنهاد شانسی", "menu:random"))
    kb.row(btn("⬅️  بازگشت", "nav:back"), btn("🏠  خانه", "nav:home"))
    return kb

from telebot import types


def nav_row(back_callback: str = "nav:back", home_callback: str = "nav:home") -> list[types.InlineKeyboardButton]:
    return [
        types.InlineKeyboardButton("⬅️ بازگشت", callback_data=back_callback),
        types.InlineKeyboardButton("🏠 خانه", callback_data=home_callback),
    ]


def pagination_row(prefix: str, page: int, total_pages: int) -> list[types.InlineKeyboardButton] | None:
    if total_pages <= 1:
        return None
    buttons = []
    if page > 1:
        buttons.append(types.InlineKeyboardButton("⬅️ قبلی", callback_data=f"page:{prefix}:{page - 1}"))
    buttons.append(types.InlineKeyboardButton(f"{page} / {total_pages}", callback_data="noop"))
    if page < total_pages:
        buttons.append(types.InlineKeyboardButton("بعدی ➡️", callback_data=f"page:{prefix}:{page + 1}"))
    return buttons


def error_keyboard(retry_callback: str = "nav:home") -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("🔄 تلاش دوباره", callback_data=retry_callback),
        types.InlineKeyboardButton("🏠 صفحه اصلی", callback_data="nav:home"),
    )
    return kb

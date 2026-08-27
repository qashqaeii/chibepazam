from telebot import types

from bot.keyboards.navigation import nav_row, pagination_row


def btn(text: str, callback_data: str) -> types.InlineKeyboardButton:
    """Standard glass-style inline button."""
    return types.InlineKeyboardButton(text, callback_data=callback_data)


def append_nav(kb: types.InlineKeyboardMarkup, back: str = "nav:back", home: str = "nav:home") -> types.InlineKeyboardMarkup:
    kb.row(*nav_row(back, home))
    return kb


def append_pagination(kb: types.InlineKeyboardMarkup, prefix: str, page: int, total_pages: int) -> types.InlineKeyboardMarkup:
    pag = pagination_row(prefix, page, total_pages)
    if pag:
        kb.row(*pag)
    return kb

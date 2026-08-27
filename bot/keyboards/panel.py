from telebot import types

from bot.keyboards.builder import btn


def panel_home_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(btn("📢  مدیریت تبلیغات", "panel:promo"))
    kb.add(btn("👑  پنل کامل ربات", "admin:main"))
    kb.add(btn("🏠  بستن", "nav:home"))
    return kb


def panel_promo_keyboard(is_active: bool) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=1)
    toggle = "🔴  غیرفعال کردن" if is_active else "🟢  فعال کردن"
    kb.add(btn(toggle, "panel:promo:toggle"))
    kb.add(btn("✏️  ویرایش متن تبلیغ", "panel:promo:edit:text"))
    kb.add(btn("🏷  ویرایش عنوان دکمه", "panel:promo:edit:btn"))
    kb.add(btn("🔗  ویرایش لینک", "panel:promo:edit:url"))
    kb.add(btn("👁  پیش‌نمایش منوی اصلی", "panel:promo:preview"))
    kb.add(btn("⬅️  بازگشت", "panel:main"))
    return kb

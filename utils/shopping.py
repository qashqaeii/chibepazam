"""Shopping-list text for sharing missing ingredients with a shopper."""

from urllib.parse import quote

_FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def to_fa_digits(value: int | str) -> str:
    return str(value).translate(_FA_DIGITS)


def ingredient_qty(item: dict) -> str:
    return " ".join(
        part for part in (item.get("amount") or "", item.get("unit") or "") if part
    ).strip()


def build_shopping_list(recipe: dict, missing: list[dict], servings: int | None = None) -> str:
    name = recipe.get("name") or "غذا"
    target = servings or recipe.get("display_servings") or recipe.get("servings") or 4
    count = len(missing)
    lines = [
        "🛒 لیست خرید",
        "",
        "سلام،",
        f"برای تهیه «{name}» این مواد را لازم داریم.",
        "لطفاً در صورت امکان تهیه بفرمایید.",
        "",
        f"🍽 غذا: {name}",
        f"👥 مناسب برای: {to_fa_digits(target)} نفر",
        f"📦 تعداد اقلام: {to_fa_digits(count)} مورد",
        "",
        "────────────",
        "مواد موردنیاز:",
    ]
    for i, item in enumerate(missing, start=1):
        qty = ingredient_qty(item)
        emoji = item.get("emoji") or "▫️"
        item_name = item.get("name") or "ماده"
        extra = f" — {qty}" if qty else ""
        lines.append(f"{to_fa_digits(i)}. {emoji} {item_name}{extra}")
    lines.extend(
        [
            "────────────",
            "",
            "نکته: مقدارها مطابق دستور پخت و تقریبی است.",
            "اگر جایگزینی لازم شد، قبل از خرید هماهنگ کنید.",
            "",
            "با تشکر 🌿",
        ]
    )
    return "\n".join(lines)


def build_share_url(plain_text: str, bot_username: str | None = None) -> str | None:
    """Native Telegram “Send to…” link. None if too long for a button URL."""
    username = (bot_username or "").lstrip("@").strip() or "share"
    bot_url = f"https://t.me/{username}"
    url = f"https://t.me/share/url?url={quote(bot_url, safe='')}&text={quote(plain_text, safe='')}"
    if len(url) > 2000:
        return None
    return url


def merge_amounts(a: str | None, b: str | None) -> str | None:
    from utils.servings import _normalize_number, _format_number

    if not a:
        return b
    if not b:
        return a
    if a == b:
        return a
    try:
        from fractions import Fraction

        va = float(Fraction(_normalize_number(a)))
        vb = float(Fraction(_normalize_number(b)))
        return _format_number(va + vb)
    except (ValueError, ZeroDivisionError):
        return f"{a} + {b}"


def build_merged_shopping_list(recipe_names: list[str], items: list[dict], servings: int) -> str:
    count = len(items)
    lines = [
        "🛒 لیست خرید ترکیبی",
        "",
        "سلام،",
        "برای تهیه این غذاها مواد زیر لازم است:",
        "",
        "🍽 " + "، ".join(recipe_names[:5]) + ("…" if len(recipe_names) > 5 else ""),
        f"👥 مناسب برای: {to_fa_digits(servings)} نفر",
        f"📦 تعداد اقلام: {to_fa_digits(count)} مورد",
        "",
        "────────────",
        "مواد موردنیاز:",
    ]
    for i, item in enumerate(items, start=1):
        qty = ingredient_qty(item)
        emoji = item.get("emoji") or "▫️"
        item_name = item.get("name") or "ماده"
        extra = f" — {qty}" if qty else ""
        lines.append(f"{to_fa_digits(i)}. {emoji} {item_name}{extra}")
    lines.extend(["────────────", "", "با تشکر 🌿"])
    return "\n".join(lines)

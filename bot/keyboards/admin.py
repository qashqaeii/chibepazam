from telebot import types

from bot.keyboards.builder import btn


def admin_dashboard_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        btn("🍲  غذاها", "admin:recipes"),
        btn("🥕  مواد", "admin:ingredients"),
    )
    kb.add(
        btn("📂  دسته‌ها", "admin:categories"),
        btn("🔄  جایگزین‌ها", "admin:substitutes"),
    )
    kb.add(
        btn("📊  Analytics", "admin:stats"),
        btn("❤️  محبوب‌ها", "admin:popular"),
    )
    kb.add(
        btn("👥  کاربران", "admin:users"),
        btn("📢  همگانی", "admin:broadcast"),
    )
    kb.add(btn("🏠  خروج", "nav:home"))
    return kb


def admin_back_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.row(
        btn("⬅️  بازگشت", "admin:main"),
        btn("👑  پنل", "admin:main"),
    )
    return kb


def admin_confirm_keyboard(yes_cb: str, no_cb: str) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.row(btn("✅  تأیید", yes_cb), btn("❌  انصراف", no_cb))
    return kb


def admin_broadcast_preview_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.row(
        btn("🖼  تصویر", "admin:bc:photo"),
        btn("🔗  دکمه", "admin:bc:button"),
    )
    kb.row(
        btn("✅  ارسال", "admin:bc:confirm"),
        btn("❌  لغو", "admin:bc:cancel"),
    )
    return kb


def admin_recipes_keyboard(recipes: list[dict], page: int, total_pages: int) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=1)
    for r in recipes:
        mark = "✅" if r.get("is_active") else "❌"
        kb.add(btn(f"{mark} {r.get('emoji','🍲')} {r['name']}", f"admin:rtog:{r['id']}:{page}"))
    if total_pages > 1:
        row = []
        if page > 1:
            row.append(btn("⬅️", f"admin:recipes:{page - 1}"))
        row.append(btn(f"{page}/{total_pages}", "noop"))
        if page < total_pages:
            row.append(btn("➡️", f"admin:recipes:{page + 1}"))
        kb.row(*row)
    kb.row(btn("⬅️  پنل", "admin:main"))
    return kb


def admin_ingredients_keyboard(items: list[dict], page: int, total_pages: int) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    for i in range(0, len(items), 2):
        row = []
        for ing in items[i : i + 2]:
            mark = "✅" if ing.get("is_active") else "❌"
            row.append(btn(f"{mark} {ing['emoji']} {ing['name'][:12]}", f"admin:itog:{ing['id']}:{page}"))
        kb.row(*row)
    if total_pages > 1:
        row = []
        if page > 1:
            row.append(btn("⬅️", f"admin:ingredients:{page - 1}"))
        row.append(btn(f"{page}/{total_pages}", "noop"))
        if page < total_pages:
            row.append(btn("➡️", f"admin:ingredients:{page + 1}"))
        kb.row(*row)
    kb.row(btn("⬅️  پنل", "admin:main"))
    return kb


def admin_categories_keyboard(categories: list[dict]) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    for i in range(0, len(categories), 2):
        row = []
        for c in categories[i : i + 2]:
            mark = "✅" if c.get("is_active") else "❌"
            row.append(btn(f"{mark} {c['emoji']} {c['name']}", f"admin:ctog:{c['id']}"))
        kb.row(*row)
    kb.row(btn("⬅️  پنل", "admin:main"))
    return kb


def admin_substitutes_keyboard(subs: list[dict]) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=1)
    for s in subs[:20]:
        label = f"{s.get('from_name','?')} → {s.get('to_name','?')}"
        kb.add(btn(f"🗑 {label[:40]}", f"admin:subdel:{s['id']}"))
    kb.row(btn("⬅️  پنل", "admin:main"))
    return kb

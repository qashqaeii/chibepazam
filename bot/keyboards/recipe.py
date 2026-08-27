from telebot import types

from bot.keyboards.builder import btn, append_nav


def forbidden_keyboard(ingredients: list[dict], selected_ids: set[int], page: int, total_pages: int) -> types.InlineKeyboardMarkup:
    from bot.keyboards.builder import append_pagination
    from utils.pagination import paginate
    from config import Config

    page_items, current_page, total_pages = paginate(ingredients, page, Config.INGREDIENTS_PER_PAGE)
    kb = types.InlineKeyboardMarkup(row_width=2)
    for i in range(0, len(page_items), 2):
        row = []
        for ing in page_items[i : i + 2]:
            mark = "🚫" if ing["id"] in selected_ids else "⬜"
            row.append(btn(f"{mark} {ing['emoji']} {ing['name']}", f"settings:forb:{ing['id']}:{current_page}"))
        kb.row(*row)
    append_pagination(kb, "forb", current_page, total_pages)
    return append_nav(kb, back="menu:settings")


def rating_keyboard(recipe_id: int, current: str | None = None) -> types.InlineKeyboardMarkup:
    opts = [("love", "😍"), ("good", "🙂"), ("ok", "😐"), ("bad", "👎")]
    kb = types.InlineKeyboardMarkup(row_width=4)
    row = []
    for key, emoji in opts:
        mark = "✓" if key == current else ""
        row.append(btn(f"{mark}{emoji}", f"recipe:rate:{recipe_id}:{key}"))
    kb.row(*row)
    kb.add(btn("⬅️  بازگشت به غذا", f"recipe:view:{recipe_id}:b"))
    return kb


def recipe_detail_keyboard(recipe_id: int, is_favorite: bool, is_disliked: bool = False, cart_count: int = 0) -> types.InlineKeyboardMarkup:
    fav_text = "💔  حذف علاقه‌مندی" if is_favorite else "❤️  ذخیره"
    dislike_text = "✅  پیشنهاد مجدد" if is_disliked else "🚫  پیشنهاد نده"
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        btn("🥕  مواد لازم", f"recipe:ingredients:{recipe_id}"),
        btn("👨‍🍳  دستور پخت", f"recipe:steps:{recipe_id}"),
    )
    kb.add(
        btn("🛒  ندارم", f"recipe:missing:{recipe_id}"),
        btn(fav_text, f"recipe:favorite:{recipe_id}"),
    )
    kb.add(
        btn("⭐  امتیاز", f"recipe:ratemenu:{recipe_id}"),
        btn("🍽  پختمش", f"recipe:cooked:{recipe_id}"),
    )
    kb.add(
        btn("🔄  جایگزین مواد", f"recipe:subst:{recipe_id}"),
        btn("🔄  مشابه", f"recipe:similar:{recipe_id}"),
    )
    cart_label = f"🛒  افزودن به لیست ({cart_count})" if cart_count else "🛒  افزودن به لیست خرید"
    kb.add(
        btn(cart_label, f"recipe:cartadd:{recipe_id}"),
        btn(dislike_text, f"recipe:dislike:{recipe_id}"),
    )
    kb.add(btn("📤  اشتراک", f"recipe:share:{recipe_id}"))
    return append_nav(kb)


def recipe_steps_keyboard(recipe_id: int, page: int = 1, total_pages: int = 1) -> types.InlineKeyboardMarkup:
    from bot.keyboards.builder import append_pagination

    kb = types.InlineKeyboardMarkup(row_width=2)
    append_pagination(kb, f"rst:{recipe_id}", page, total_pages)
    kb.add(btn("⬅️  بازگشت به غذا", f"recipe:view:{recipe_id}:b"))
    kb.add(btn("🏠  خانه", "nav:home"))
    return kb


def recipe_missing_keyboard(
    recipe_id: int,
    has_missing: bool,
    share_url: str | None = None,
) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=1)
    if has_missing:
        kb.add(btn("📤  ارسال لیست خرید", f"recipe:buylist:{recipe_id}"))
        if share_url:
            kb.add(types.InlineKeyboardButton("📲  ارسال به خریدار", url=share_url))
    kb.add(btn("⬅️  بازگشت به غذا", f"recipe:view:{recipe_id}:b"))
    kb.add(btn("🏠  خانه", "nav:home"))
    return kb


def shopping_message_keyboard(recipe_id: int, share_url: str | None = None) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=1)
    if share_url:
        kb.add(types.InlineKeyboardButton("📲  ارسال به خریدار", url=share_url))
    kb.add(btn("⬅️  بازگشت به غذا", f"recipe:view:{recipe_id}:b"))
    return kb


def recipe_sub_keyboard(recipe_id: int) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(btn("⬅️  بازگشت به غذا", f"recipe:view:{recipe_id}:b"))
    kb.add(btn("🏠  خانه", "nav:home"))
    return kb


def recipe_list_keyboard(recipes: list[dict], prefix: str = "recipe:view") -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=1)
    for r in recipes:
        kb.add(btn(f"{r.get('emoji', '🍲')}  {r['name']}", f"{prefix}:{r['id']}"))
    return append_nav(kb)


def recommend_list_keyboard(items: list[dict]) -> types.InlineKeyboardMarkup:
    from utils.telegram import match_emoji

    kb = types.InlineKeyboardMarkup(row_width=1)
    for item in items:
        recipe = item["recipe"]
        score = item["score"]
        emoji = match_emoji(score)
        kb.add(
            btn(
                f"{emoji}  {recipe['name']}  —  {score:.0f}٪",
                f"recipe:view:{recipe['id']}",
            )
        )
    return kb


def favorites_keyboard(recipes: list[dict], page: int, total_pages: int) -> types.InlineKeyboardMarkup:
    from bot.keyboards.builder import append_pagination

    kb = types.InlineKeyboardMarkup(row_width=1)
    for r in recipes:
        kb.add(btn(f"{r.get('emoji', '🍲')}  {r['name']}", f"recipe:view:{r['id']}"))
    append_pagination(kb, "fav", page, total_pages)
    return append_nav(kb)

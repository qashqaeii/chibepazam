from telebot import TeleBot

from bot.handlers.base import safe_edit, show_error, answer_callback
from bot.keyboards.pantry import (
    pantry_main_keyboard,
    pantry_category_keyboard,
    pantry_selected_keyboard,
    pantry_clear_confirm_keyboard,
    recommend_keyboard,
)
from bot.keyboards.recipe import recommend_list_keyboard
from services.ingredient_service import IngredientService
from services.recommendation_service import RecommendationService
from services.user_service import UserService
from services.nav_service import nav_service
from utils.screen import build_screen, list_body, ACTION_FOOTER
from utils.telegram import esc


from services.filter_presets import RECOMMEND_FILTERS

ingredient_service = IngredientService()
recommendation_service = RecommendationService()
user_service = UserService()


def show_pantry_main(bot: TeleBot, chat_id: int, message_id: int, user_id: int) -> None:
    categories = ingredient_service.get_categories()
    count = ingredient_service.pantry_count(user_id)
    permanent = len(ingredient_service.get_permanent_ids(user_id))
    text = build_screen(
        emoji="🧺",
        title="مواد داخل خونه",
        description=[
            "موادی که الان در دسترس داری رو از دسته‌ها انتخاب کن.",
            "ادویه و روغن همیشگی را از تنظیمات مشخص کن.",
        ],
        details=[
            f"✅  انتخاب‌شده: <b>{count}</b> مورد",
            f"🏠  مواد همیشگی: <b>{permanent}</b> مورد",
            f"📂  دسته‌بندی: <b>{len(categories)}</b> دسته",
            f"🥕  مواد قابل انتخاب: <b>{sum(c.get('item_count') or 0 for c in categories)}</b> مورد",
        ],
    )
    safe_edit(bot, chat_id, message_id, text, pantry_main_keyboard(categories, count))


def show_pantry_category(
    bot: TeleBot, chat_id: int, message_id: int, user_id: int, category_id: int, page: int = 1
) -> None:
    category = ingredient_service.get_category(category_id)
    if not category:
        return
    ingredients = ingredient_service.get_by_category(category_id)
    selected = ingredient_service.get_selected_ids(user_id)
    count = len(selected & {i["id"] for i in ingredients})

    text = build_screen(
        emoji=category["emoji"],
        title=category["name"],
        description=[
            "روی هر ماده بزن تا انتخاب/لغو بشه.",
            "✅ = داری  ·  ⬜ = نداری",
        ],
        details=[
            f"📋  از این دسته: <b>{count}</b> مورد انتخاب شده",
            f"🥕  کل مواد دسته: <b>{len(ingredients)}</b> مورد",
        ],
        footer="👇 مواد رو انتخاب کن، بعد «تأیید» بزن",
        escape_title=False,
    )
    safe_edit(
        bot, chat_id, message_id, text,
        pantry_category_keyboard(category, ingredients, selected, page),
    )


def show_pantry_selected(bot: TeleBot, chat_id: int, message_id: int, user_id: int) -> None:
    items = ingredient_service.get_selected_ingredients(user_id)
    if not items:
        text = build_screen(
            emoji="📋",
            title="انتخاب‌های من",
            description=[
                "هنوز ماده‌ای انتخاب نکردی.",
                "از منوی قبل مواد خونه‌ات رو اضافه کن.",
            ],
            footer="👇 برای افزودن مواد برگرد",
        )
    else:
        lines = [f"{i['emoji']}  {esc(i['name'])}" for i in items]
        text = build_screen(
            emoji="📋",
            title="مواد فعلی من",
            description=f"شما <b>{len(items)}</b> ماده انتخاب کرده‌اید:",
            body=list_body(lines),
            footer=ACTION_FOOTER,
        )
    safe_edit(bot, chat_id, message_id, text, pantry_selected_keyboard())


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


def _active_filter_keys(user_id: int) -> set[str]:
    cur = nav_service.get_current(user_id)
    if not cur:
        return set()
    return set((cur.get("payload") or {}).get("active_filters") or [])


def _merge_filters(keys: set[str]) -> dict:
    merged: dict = {}
    for key in keys:
        preset = RECOMMEND_FILTERS.get(key, {})
        for k, v in preset.items():
            if k == "category_slugs" and k in merged:
                merged[k] = list(set(merged[k]) | set(v))
            else:
                merged[k] = v
    return merged


def show_recommend_filters(bot: TeleBot, chat_id: int, message_id: int, user_id: int) -> None:
    from telebot import types
    from bot.keyboards.builder import btn, append_nav

    active = _active_filter_keys(user_id)
    lines = [f"{'✅' if k in active else '⬜'} {FILTER_LABELS[k]}" for k in FILTER_LABELS]
    text = build_screen(
        emoji="🎛",
        title="فیلتر پیشنهاد",
        description="فیلترها را انتخاب کن، بعد «نمایش نتایج» را بزن.",
        body=list_body(lines),
        footer="👇 فیلتر را روشن/خاموش کن",
    )
    kb = types.InlineKeyboardMarkup(row_width=2)
    for key in ("time_short", "time_medium", "cost_low", "cost_high"):
        mark = "✅" if key in active else "⬜"
        kb.add(btn(f"{mark} {FILTER_LABELS[key]}", f"pantry:flt:{key}"))
    for key in ("meal_polo", "meal_stew", "meal_kebab", "meal_ash"):
        mark = "✅" if key in active else "⬜"
        kb.row(
            btn(f"{mark} {FILTER_LABELS[key]}", f"pantry:flt:{key}"),
        )
    kb.row(
        btn(f"{'✅' if 'veg_only' in active else '⬜'} گیاهی", "pantry:flt:veg_only"),
        btn(f"{'✅' if 'vegan_only' in active else '⬜'} وگان", "pantry:flt:vegan_only"),
    )
    kb.row(
        btn(f"{'✅' if 'available_now' in active else '⬜'} همین الان", "pantry:flt:available_now"),
        btn(f"{'✅' if 'one_missing' in active else '⬜'} ۱ ماده کم", "pantry:flt:one_missing"),
    )
    kb.add(btn("🔥  نمایش نتایج", "pantry:recgo"))
    kb.add(btn("🗑  پاک کردن فیلترها", "pantry:fltclr"))
    safe_edit(bot, chat_id, message_id, text, append_nav(kb, back="pantry:main"))


def show_recommendations(bot: TeleBot, chat_id: int, message_id: int, user_id: int, page: int = 1) -> None:
    active = _active_filter_keys(user_id)
    filters = _merge_filters(active) if active else {}
    items, current_page, total_pages = recommendation_service.get_recommendations(
        user_id, page, filters=filters or None,
    )
    count = ingredient_service.pantry_count(user_id)

    if not items:
        if count == 0:
            text = build_screen(
                emoji="🍽",
                title="پیشنهادهای مناسب",
                description=[
                    "اول مواد خونه‌ات رو انتخاب کن.",
                    "بعد بهترین غذاها رو بهت پیشنهاد می‌دم.",
                ],
            )
        else:
            text = build_screen(
                emoji="🍽",
                title="پیشنهادهای مناسب",
                description=[
                    "متأسفانه غذای مناسبی پیدا نشد.",
                    "مواد بیشتری اضافه کن یا ترکیب رو تغییر بده.",
                ],
                details=[f"📋  مواد انتخاب‌شده: <b>{count}</b> مورد"],
            )
        safe_edit(bot, chat_id, message_id, text, pantry_main_keyboard(
            ingredient_service.get_categories(), count
        ))
        return

    text = build_screen(
        emoji="🔥",
        title="پیشنهادهای مناسب برای شما",
        description=[
            f"بر اساس <b>{count}</b> ماده‌ای که انتخاب کردی،",
            "این غذاها بیشترین تطابق رو دارن:",
        ],
        details=[f"📄  صفحه <b>{current_page}</b> از <b>{total_pages}</b>"] if total_pages > 1 else None,
        footer="👇 روی غذا بزن برای جزئیات",
    )
    kb = recommend_list_keyboard(items)
    for row in recommend_keyboard(current_page, total_pages).keyboard:
        kb.row(*row)
    safe_edit(bot, chat_id, message_id, text, kb)


def register_pantry_handlers(bot: TeleBot) -> None:
    @bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("pantry:"))
    def handle_pantry(call):
        user = user_service.get_user(call.from_user.id)
        if not user:
            answer_callback(bot, call)
            return

        user_id = user["id"]
        chat_id = call.message.chat.id
        msg_id = call.message.message_id
        parts = call.data.split(":")
        action = parts[1]

        if action != "recommend":
            answer_callback(bot, call)

        try:
            if action == "main":
                show_pantry_main(bot, chat_id, msg_id, user_id)

            elif action == "category":
                category_id = int(parts[2])
                nav_service.navigate(user_id, "pantry_category", {"category_id": category_id, "page": 1})
                show_pantry_category(bot, chat_id, msg_id, user_id, category_id)

            elif action == "ingredient":
                ingredient_id = int(parts[2])
                category_id = int(parts[3])
                page = int(parts[4]) if len(parts) > 4 else 1
                ingredient_service.toggle_pantry(user_id, ingredient_id)
                nav_service.replace(user_id, "pantry_category", {"category_id": category_id, "page": page})
                show_pantry_category(bot, chat_id, msg_id, user_id, category_id, page)

            elif action == "done":
                show_pantry_main(bot, chat_id, msg_id, user_id)

            elif action == "selected":
                nav_service.navigate(user_id, "pantry_selected", {})
                show_pantry_selected(bot, chat_id, msg_id, user_id)

            elif action == "clear":
                if len(parts) > 2 and parts[2] == "yes":
                    ingredient_service.clear_pantry(user_id)
                    show_pantry_main(bot, chat_id, msg_id, user_id)
                else:
                    text = build_screen(
                        emoji="🗑",
                        title="پاک کردن مواد",
                        description="همه مواد انتخاب‌شده پاک شوند؟",
                        footer="👇 تأیید یا انصراف",
                    )
                    safe_edit(bot, chat_id, msg_id, text, pantry_clear_confirm_keyboard())

            elif action == "recommend":
                answer_callback(bot, call, "فیلترها را تنظیم کن 🎛")
                nav_service.navigate(user_id, "recommend_filters", {"active_filters": list(_active_filter_keys(user_id))})
                show_recommend_filters(bot, chat_id, msg_id, user_id)
                return

            elif action == "flt":
                key = parts[2]
                cur = nav_service.get_current(user_id) or {"payload": {}}
                active = set(cur.get("payload", {}).get("active_filters") or [])
                if key in active:
                    active.discard(key)
                else:
                    active.add(key)
                nav_service.replace(user_id, "recommend_filters", {"active_filters": list(active)})
                show_recommend_filters(bot, chat_id, msg_id, user_id)

            elif action == "fltclr":
                nav_service.replace(user_id, "recommend_filters", {"active_filters": []})
                show_recommend_filters(bot, chat_id, msg_id, user_id)

            elif action == "recgo":
                answer_callback(bot, call, "دارم بهترین غذاها رو پیدا می‌کنم... 🍲")
                active = _active_filter_keys(user_id)
                nav_service.navigate(user_id, "recommendations", {"page": 1, "active_filters": list(active)})
                show_recommendations(bot, chat_id, msg_id, user_id)
                return

        except Exception as e:
            from utils.logger import setup_logger
            setup_logger(__name__).exception("pantry handler error: %s", e)
            show_error(bot, call, "pantry:main")

    @bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("page:rec:"))
    def handle_rec_page(call):
        answer_callback(bot, call)
        user = user_service.get_user(call.from_user.id)
        if not user:
            return
        page = int(call.data.split(":")[2])
        nav_service.replace(user["id"], "recommendations", {"page": page, "active_filters": list(_active_filter_keys(user["id"]))})
        show_recommendations(bot, call.message.chat.id, call.message.message_id, user["id"], page)

    @bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("page:ing:"))
    def handle_ing_page(call):
        answer_callback(bot, call)
        user = user_service.get_user(call.from_user.id)
        if not user:
            return
        parts = call.data.split(":")
        category_id = int(parts[2])
        page = int(parts[3])
        nav_service.replace(user["id"], "pantry_category", {"category_id": category_id, "page": page})
        show_pantry_category(bot, call.message.chat.id, call.message.message_id, user["id"], category_id, page)

from telebot import TeleBot

from bot.handlers.base import safe_edit, show_error, answer_callback
from bot.keyboards.pantry import (
    pantry_main_keyboard,
    pantry_category_keyboard,
    pantry_selected_keyboard,
    pantry_clear_confirm_keyboard,
    recommend_keyboard,
    recommend_filters_keyboard,
    FILTER_LABELS,
)
from bot.keyboards.recipe import recommend_list_keyboard
from services.ingredient_service import IngredientService
from services.recommendation_service import RecommendationService
from services.user_service import UserService
from services.nav_service import nav_service
from utils.screen import build_screen, list_body, ACTION_FOOTER
from utils.menu_style import section, join_sections, status_chip
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
            "مواد موجود را از دسته‌ها انتخاب کن تا پیشنهاد دقیق‌تری بگیری.",
            "نمک، روغن و ادویه‌های همیشگی را از تنظیمات مشخص کن.",
        ],
        details=[
            status_chip("انتخاب‌شده", count, "✅"),
            status_chip("مواد همیشگی", permanent, "🏠"),
            status_chip("دسته‌بندی", len(categories), "📂"),
            status_chip("مواد قابل انتخاب", sum(c.get("item_count") or 0 for c in categories), "🥕"),
        ],
        footer="👇 دسته مورد نظر را باز کن",
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
            "روی هر ماده بزن تا انتخاب یا لغو شود.",
            "علامت ✅ یعنی داری  ·  ⬜ یعنی نداری",
        ],
        details=[
            status_chip("انتخاب از این دسته", count, "📋"),
            status_chip("کل مواد دسته", len(ingredients), "🥕"),
        ],
        footer="👇 مواد را انتخاب کن، سپس «تأیید و بازگشت»",
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
                "از دسته‌ها مواد موجود در آشپزخانه را اضافه کن.",
            ],
            details=["💡  بعد از انتخاب، «فیلتر پیشنهاد» یا «چی می‌تونم بپزم» را بزن"],
            footer="👇 برای افزودن مواد برگرد",
        )
    else:
        lines = [f"{i['emoji']}  {esc(i['name'])}" for i in items]
        text = build_screen(
            emoji="📋",
            title="مواد فعلی من",
            description=f"بر اساس انتخاب تو، <b>{len(items)}</b> ماده فعال است:",
            body=list_body(lines),
            footer=ACTION_FOOTER,
        )
    safe_edit(bot, chat_id, message_id, text, pantry_selected_keyboard())


FILTER_SECTIONS = {
    "time": ("⏱  زمان پخت", ("time_short", "time_medium")),
    "cost": ("💰  بودجه", ("cost_low", "cost_high")),
    "meal": ("🍽  نوع غذا", ("meal_polo", "meal_stew", "meal_kebab", "meal_ash")),
    "diet": ("🌱  رژیم", ("veg_only", "vegan_only")),
    "extra": ("✨  شرایط ویژه", ("available_now", "one_missing")),
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
    active = _active_filter_keys(user_id)
    blocks = []
    for _, (title, keys) in FILTER_SECTIONS.items():
        lines = [f"{'✅' if k in active else '⬜'} {FILTER_LABELS[k]}" for k in keys]
        blocks.append(section(title, lines))
    body = join_sections(*blocks)
    active_count = len(active)
    text = build_screen(
        emoji="🎛",
        title="فیلتر پیشنهاد غذا",
        description=[
            "فیلترها را ترکیب کن تا نتیجه دقیق‌تر شود.",
            f"فیلتر فعال: <b>{active_count}</b> مورد",
        ],
        body=body,
        footer="👇 روی دکمه بزن تا روشن/خاموش شود، سپس «نمایش نتایج»",
    )
    safe_edit(bot, chat_id, message_id, text, recommend_filters_keyboard(active))


def show_recommendations(bot: TeleBot, chat_id: int, message_id: int, user_id: int, page: int = 1) -> None:
    active = _active_filter_keys(user_id)
    filters = _merge_filters(active) if active else {}
    items, current_page, total_pages = recommendation_service.get_recommendations(
        user_id, page, filters=filters or None,
    )
    count = ingredient_service.pantry_count(user_id)
    filter_note = f"🎛  فیلتر فعال: <b>{len(active)}</b>" if active else None

    if not items:
        if count == 0:
            text = build_screen(
                emoji="🍽",
                title="پیشنهادهای مناسب",
                description=[
                    "اول مواد موجود در خانه را انتخاب کن.",
                    "سپس فیلتر بزن یا مستقیم «چی می‌تونم بپزم» را بزن.",
                ],
                details=[filter_note] if filter_note else None,
                footer="👇 به «مواد داخل خونه» برگرد",
            )
        else:
            text = build_screen(
                emoji="🍽",
                title="پیشنهادهای مناسب",
                description=[
                    "با این ترکیب مواد و فیلترها، غذایی پیدا نشد.",
                    "فیلترها را سبک‌تر کن یا مواد بیشتری اضافه کن.",
                ],
                details=[
                    status_chip("مواد انتخاب‌شده", count, "📋"),
                    filter_note,
                ],
                footer="👇 فیلتر یا مواد را تغییر بده",
            )
        safe_edit(bot, chat_id, message_id, text, pantry_main_keyboard(
            ingredient_service.get_categories(), count
        ))
        return

    details = [status_chip("مواد فعال", count, "🧺")]
    if filter_note:
        details.append(filter_note)
    if total_pages > 1:
        details.append(f"📄  صفحه <b>{current_page}</b> از <b>{total_pages}</b>")

    text = build_screen(
        emoji="🔥",
        title="بهترین پیشنهادها برای تو",
        description=[
            "این غذاها بیشترین تطابق را با مواد تو دارند.",
            "درصد کنار هر غذا میزان تطابق را نشان می‌دهد.",
        ],
        details=details,
        footer="👇 روی غذا بزن برای جزئیات و دستور پخت",
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

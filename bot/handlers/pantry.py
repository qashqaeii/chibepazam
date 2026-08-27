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
from utils.telegram import esc


ingredient_service = IngredientService()
recommendation_service = RecommendationService()
user_service = UserService()


def show_pantry_main(bot: TeleBot, chat_id: int, message_id: int, user_id: int) -> None:
    categories = ingredient_service.get_categories()
    count = ingredient_service.pantry_count(user_id)
    text = (
        "🧺 <b>مواد داخل خونه</b>\n\n"
        "موادی که الان در دسترس داری رو انتخاب کن 👇\n\n"
        f"انتخاب‌شده: <b>{count}</b> مورد"
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

    text = (
        f"{category['emoji']} <b>{esc(category['name'])}</b>\n\n"
        "موادی که داری رو انتخاب کن:\n\n"
        f"انتخاب شده: <b>{count}</b> مورد"
    )
    safe_edit(
        bot,
        chat_id,
        message_id,
        text,
        pantry_category_keyboard(category, ingredients, selected, page),
    )


def show_pantry_selected(bot: TeleBot, chat_id: int, message_id: int, user_id: int) -> None:
    items = ingredient_service.get_selected_ingredients(user_id)
    if not items:
        text = (
            "🧺 <b>مواد فعلی من</b>\n\n"
            "هنوز ماده‌ای انتخاب نکردی.\n"
            "از منوی قبل مواد خونه‌ات رو اضافه کن 👇"
        )
    else:
        lines = "\n".join(f"{i['emoji']} {esc(i['name'])}" for i in items)
        text = (
            f"🧺 <b>مواد فعلی من</b>\n\n"
            f"شما <b>{len(items)}</b> ماده انتخاب کرده‌اید:\n\n"
            f"{lines}"
        )
    safe_edit(bot, chat_id, message_id, text, pantry_selected_keyboard())


def show_recommendations(bot: TeleBot, chat_id: int, message_id: int, user_id: int, page: int = 1) -> None:
    items, current_page, total_pages = recommendation_service.get_recommendations(user_id, page)

    if not items:
        count = ingredient_service.pantry_count(user_id)
        if count == 0:
            text = (
                "🍽 <b>پیشنهادهای مناسب</b>\n\n"
                "اول مواد خونه‌ات رو انتخاب کن\n"
                "تا بهترین غذاها رو پیشنهاد بدم 👇"
            )
        else:
            text = (
                "🍽 <b>پیشنهادهای مناسب</b>\n\n"
                "متأسفانه غذای مناسبی پیدا نشد.\n"
                "مواد بیشتری اضافه کن یا تغییر بده 👇"
            )
        safe_edit(bot, chat_id, message_id, text, pantry_main_keyboard(
            ingredient_service.get_categories(), count
        ))
        return

    count = ingredient_service.pantry_count(user_id)
    text = (
        "🍽 <b>پیشنهادهای مناسب برای شما</b>\n\n"
        f"بر اساس <b>{count}</b> ماده‌ای که انتخاب کردی،\n"
        "این غذاها بیشترین تطابق رو دارند 👇"
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
                category_id = int(parts[2])
                show_pantry_main(bot, chat_id, msg_id, user_id)

            elif action == "selected":
                nav_service.navigate(user_id, "pantry_selected", {})
                show_pantry_selected(bot, chat_id, msg_id, user_id)

            elif action == "clear":
                if len(parts) > 2 and parts[2] == "yes":
                    ingredient_service.clear_pantry(user_id)
                    show_pantry_main(bot, chat_id, msg_id, user_id)
                else:
                    text = "همه مواد انتخاب‌شده پاک شوند؟"
                    safe_edit(bot, chat_id, msg_id, text, pantry_clear_confirm_keyboard())

            elif action == "recommend":
                answer_callback(bot, call, "دارم بهترین غذاها رو پیدا می‌کنم... 🍲")
                nav_service.navigate(user_id, "recommendations", {"page": 1})
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
        nav_service.replace(user["id"], "recommendations", {"page": page})
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

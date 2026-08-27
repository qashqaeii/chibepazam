from telebot import TeleBot

from bot.handlers.base import safe_edit, answer_callback, show_error
from bot.keyboards.recipe import (
    recipe_detail_keyboard,
    recipe_list_keyboard,
    recipe_sub_keyboard,
    recipe_steps_keyboard,
    recipe_missing_keyboard,
    shopping_message_keyboard,
    rating_keyboard,
)
from services.recipe_service import RecipeService
from services.rating_service import RatingService, RATING_LABELS
from services.cooked_service import CookedService
from services.dislike_service import DislikeService
from services.substitute_service import SubstituteService
from services.shopping_service import ShoppingService
from services.user_service import UserService
from services.nav_service import nav_service
from utils.screen import build_screen, recipe_detail_screen, list_body, ACTION_FOOTER
from utils.telegram import esc
from utils.share import build_recipe_share_text, build_recipe_share_url


recipe_service = RecipeService()
rating_service = RatingService()
cooked_service = CookedService()
dislike_service = DislikeService()
substitute_service = SubstituteService()
shopping_service = ShoppingService()
user_service = UserService()
_bot_username: str | None = None


def _get_bot_username(bot: TeleBot) -> str:
    global _bot_username
    if _bot_username:
        return _bot_username
    try:
        _bot_username = bot.get_me().username or "Chibepazamrobot"
    except Exception:
        _bot_username = "Chibepazamrobot"
    return _bot_username


def _missing_share_url(bot: TeleBot, recipe: dict, missing: list[dict]) -> str | None:
    from utils.shopping import build_shopping_list, build_share_url

    if not missing:
        return None
    servings = recipe.get("display_servings") or recipe.get("servings") or 4
    return build_share_url(build_shopping_list(recipe, missing, servings), _get_bot_username(bot))


def show_recipe(bot: TeleBot, chat_id: int, message_id: int, user_id: int, recipe_id: int) -> None:
    recipe = recipe_service.view_recipe(user_id, recipe_id)
    if not recipe:
        return
    cart_count = shopping_service.count(user_id)
    text = recipe_detail_screen(recipe, recipe.get("match"))
    safe_edit(
        bot, chat_id, message_id, text,
        recipe_detail_keyboard(
            recipe_id,
            recipe.get("is_favorite", False),
            recipe.get("is_disliked", False),
            cart_count,
        ),
    )


def _show_steps(bot: TeleBot, chat_id: int, message_id: int, recipe_id: int, page: int = 1) -> None:
    from utils.recipe_text import paginate_instructions

    recipe = recipe_service.get_recipe(recipe_id)
    if not recipe:
        return
    raw = recipe.get("instructions") or recipe.get("description") or "دستور پخت هنوز ثبت نشده است."
    body, page, total_pages = paginate_instructions(raw, page)
    body = "\n".join(esc(line) for line in body.splitlines())
    total_time = recipe.get("prep_time", 0) + recipe.get("cook_time", 0)
    page_note = f"  ·  صفحه {page} از {total_pages}" if total_pages > 1 else ""
    text = build_screen(
        emoji="👨‍🍳",
        title=f"دستور پخت — {recipe['name']}",
        description=f"⏱  آماده‌سازی + پخت: <b>{total_time}</b> دقیقه{page_note}",
        body=body,
        footer=ACTION_FOOTER,
        escape_title=False,
    )
    safe_edit(bot, chat_id, message_id, text, recipe_steps_keyboard(recipe_id, page, total_pages))


def register_recipe_handlers(bot: TeleBot) -> None:
    @bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("recipe:"))
    def handle_recipe(call):
        user = user_service.get_user(call.from_user.id)
        if not user:
            answer_callback(bot, call)
            return

        user_id = user["id"]
        chat_id = call.message.chat.id
        msg_id = call.message.message_id
        parts = call.data.split(":")
        action = parts[1]

        try:
            if action == "view":
                answer_callback(bot, call)
                recipe_id = int(parts[2])
                from_back = len(parts) > 3 and parts[3] == "b"
                cur = nav_service.get_current(user_id)
                if from_back or (
                    cur and cur["screen"] == "recipe_detail"
                    and cur["payload"].get("recipe_id") == recipe_id
                ):
                    nav_service.replace(user_id, "recipe_detail", {"recipe_id": recipe_id})
                else:
                    nav_service.navigate(user_id, "recipe_detail", {"recipe_id": recipe_id})
                show_recipe(bot, chat_id, msg_id, user_id, recipe_id)

            elif action == "favorite":
                recipe_id = int(parts[2])
                is_fav = recipe_service.toggle_favorite(user_id, recipe_id)
                answer_callback(bot, call, "❤️ ذخیره شد" if is_fav else "💔 حذف شد")
                show_recipe(bot, chat_id, msg_id, user_id, recipe_id)

            elif action == "ratemenu":
                answer_callback(bot, call)
                recipe_id = int(parts[2])
                recipe = recipe_service.get_recipe(recipe_id)
                current = rating_service.get_user_rating(user_id, recipe_id)
                text = build_screen(
                    emoji="⭐",
                    title=f"امتیاز — {recipe['name'] if recipe else ''}",
                    description="تجربه‌ات از این غذا چطور بود؟",
                    footer="👇 یک گزینه انتخاب کن",
                    escape_title=False,
                )
                safe_edit(bot, chat_id, msg_id, text, rating_keyboard(recipe_id, current))

            elif action == "rate":
                recipe_id = int(parts[2])
                rating_key = parts[3]
                rating_service.set_rating(user_id, recipe_id, rating_key)
                answer_callback(bot, call, RATING_LABELS.get(rating_key, "ثبت شد"))
                show_recipe(bot, chat_id, msg_id, user_id, recipe_id)

            elif action == "cooked":
                recipe_id = int(parts[2])
                count = cooked_service.mark_cooked(user_id, recipe_id)
                answer_callback(bot, call, f"🍽 ثبت شد ({count} بار)")
                show_recipe(bot, chat_id, msg_id, user_id, recipe_id)

            elif action == "dislike":
                recipe_id = int(parts[2])
                active = dislike_service.toggle(user_id, recipe_id)
                answer_callback(bot, call, "🚫 دیگر پیشنهاد نمی‌شود" if active else "✅ دوباره پیشنهاد می‌شود")
                show_recipe(bot, chat_id, msg_id, user_id, recipe_id)

            elif action == "subst":
                answer_callback(bot, call)
                recipe_id = int(parts[2])
                lines = substitute_service.format_lines(recipe_id)
                body = list_body(lines, "جایگزینی برای این غذا ثبت نشده است.")
                recipe = recipe_service.get_recipe(recipe_id)
                text = build_screen(
                    emoji="🔄",
                    title=f"جایگزین مواد — {recipe['name'] if recipe else ''}",
                    body=body,
                    footer=ACTION_FOOTER,
                    escape_title=False,
                )
                safe_edit(bot, chat_id, msg_id, text, recipe_sub_keyboard(recipe_id))

            elif action == "cartadd":
                recipe_id = int(parts[2])
                n = shopping_service.add_recipe(user_id, recipe_id)
                answer_callback(bot, call, f"🛒 به لیست اضافه شد ({n} غذا)")
                show_recipe(bot, chat_id, msg_id, user_id, recipe_id)

            elif action == "ingredients":
                answer_callback(bot, call)
                recipe_id = int(parts[2])
                recipe = recipe_service.get_recipe_detail(recipe_id, user_id)
                if not recipe:
                    return
                from services.ingredient_service import IngredientService
                combined = IngredientService().get_combined_ids(user_id)
                servings = recipe.get("display_servings") or 4
                lines = [f"👥 مقادیر برای <b>{servings}</b> نفر:", ""]
                for ri in recipe.get("ingredients", []):
                    mark = "✅" if ri["ingredient_id"] in combined else "❌"
                    qty = " ".join(
                        part for part in (ri.get("amount") or "", ri.get("unit") or "") if part
                    ).strip()
                    optional = "  ·  اختیاری" if ri.get("is_optional") else ""
                    amount = f" — {qty}{optional}" if qty or optional else ""
                    lines.append(f"{mark}  {ri['emoji']} {esc(ri['name'])}{amount}")
                have = sum(1 for ri in recipe.get("ingredients", []) if ri["ingredient_id"] in combined)
                total = len(recipe.get("ingredients", []))
                text = build_screen(
                    emoji="🥕",
                    title=f"مواد لازم — {recipe['name']}",
                    description=f"از <b>{total}</b> ماده، <b>{have}</b> مورد رو داری.",
                    body=list_body(lines),
                    footer=ACTION_FOOTER,
                    escape_title=False,
                )
                safe_edit(bot, chat_id, msg_id, text, recipe_sub_keyboard(recipe_id))

            elif action == "steps":
                answer_callback(bot, call)
                recipe_id = int(parts[2])
                page = int(parts[3]) if len(parts) > 3 else 1
                _show_steps(bot, chat_id, msg_id, recipe_id, page)

            elif action == "missing":
                answer_callback(bot, call)
                recipe_id = int(parts[2])
                recipe = recipe_service.get_recipe_detail(recipe_id, user_id)
                if not recipe or not recipe.get("match"):
                    return
                from utils.shopping import ingredient_qty

                missing = recipe["match"].missing_ingredients
                if not missing:
                    body = "🎉  همه مواد لازم رو داری!\nمی‌تونی همین الان شروع به پخت کنی."
                else:
                    lines = []
                    for m in missing:
                        qty = ingredient_qty(m)
                        amount = f" — {qty}" if qty else ""
                        lines.append(f"❌  {m['emoji']} {esc(m['name'])}{amount}")
                    body = list_body(lines)
                text = build_screen(
                    emoji="🛒",
                    title="چیزایی که ندارم",
                    description=f"برای «{esc(recipe['name'])}» این مواد کم داری:",
                    body=body,
                    footer="👇 لیست خرید را برای خریدار بفرست" if missing else ACTION_FOOTER,
                    escape_title=False,
                )
                safe_edit(
                    bot, chat_id, msg_id, text,
                    recipe_missing_keyboard(recipe_id, bool(missing), _missing_share_url(bot, recipe, missing)),
                )

            elif action == "buylist":
                recipe_id = int(parts[2])
                recipe = recipe_service.get_recipe_detail(recipe_id, user_id)
                if not recipe or not recipe.get("match"):
                    answer_callback(bot, call)
                    return
                missing = recipe["match"].missing_ingredients
                if not missing:
                    answer_callback(bot, call, "همه مواد رو داری 🎉")
                    return
                from utils.shopping import build_shopping_list

                servings = recipe.get("display_servings") or 4
                plain = build_shopping_list(recipe, missing, servings)
                share_url = _missing_share_url(bot, recipe, missing)
                answer_callback(bot, call, "لیست خرید آماده شد ✅")
                try:
                    bot.send_message(
                        chat_id,
                        plain,
                        reply_markup=shopping_message_keyboard(recipe_id, share_url),
                        disable_web_page_preview=True,
                    )
                except Exception:
                    from utils.logger import setup_logger
                    setup_logger(__name__).exception("shopping list send failed")

            elif action == "similar":
                answer_callback(bot, call)
                recipe_id = int(parts[2])
                nav_service.push_current(user_id)
                similar = recipe_service.get_similar(recipe_id)
                if not similar:
                    text = build_screen(
                        emoji="🔄", title="غذاهای مشابه",
                        description="غذای مشابهی پیدا نشد.", footer=ACTION_FOOTER,
                    )
                    safe_edit(bot, chat_id, msg_id, text, recipe_sub_keyboard(recipe_id))
                else:
                    nav_service.set_current(user_id, "recipe_similar", {"recipe_id": recipe_id})
                    text = build_screen(
                        emoji="🔄", title="غذاهای مشابه",
                        description="این غذاها به غذای انتخابی شما نزدیک‌ترن:",
                        details=[f"📋  {len(similar)} پیشنهاد"], footer="👇 روی غذا بزن",
                    )
                    safe_edit(bot, chat_id, msg_id, text, recipe_list_keyboard(similar))

            elif action == "share":
                answer_callback(bot, call)
                recipe_id = int(parts[2])
                recipe = recipe_service.get_recipe(recipe_id)
                if recipe:
                    share_url = build_recipe_share_url(recipe, _get_bot_username(bot))
                    text = build_recipe_share_text(recipe, _get_bot_username(bot))
                    if share_url:
                        from telebot import types
                        kb = types.InlineKeyboardMarkup()
                        kb.add(types.InlineKeyboardButton("📲  اشتراک در تلگرام", url=share_url))
                        bot.send_message(chat_id, text, reply_markup=kb, disable_web_page_preview=True)
                    else:
                        bot.send_message(chat_id, text, disable_web_page_preview=True)
            else:
                answer_callback(bot, call)

        except Exception as e:
            from utils.logger import setup_logger
            setup_logger(__name__).exception("recipe handler error: %s", e)
            answer_callback(bot, call)
            show_error(bot, call, "nav:home")

    @bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("page:rst:"))
    def handle_steps_page(call):
        answer_callback(bot, call)
        user = user_service.get_user(call.from_user.id)
        if not user:
            return
        parts = call.data.split(":")
        recipe_id = int(parts[2])
        page = int(parts[3])
        _show_steps(bot, call.message.chat.id, call.message.message_id, recipe_id, page)

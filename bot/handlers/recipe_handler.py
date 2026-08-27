from telebot import TeleBot

from bot.handlers.base import safe_edit, answer_callback, show_error
from bot.keyboards.recipe import recipe_detail_keyboard, recipe_list_keyboard, recipe_sub_keyboard
from services.recipe_service import RecipeService
from services.user_service import UserService
from services.nav_service import nav_service
from utils.screen import build_screen, recipe_detail_screen, list_body, ACTION_FOOTER
from utils.telegram import esc


recipe_service = RecipeService()
user_service = UserService()


def show_recipe(bot: TeleBot, chat_id: int, message_id: int, user_id: int, recipe_id: int) -> None:
    recipe = recipe_service.view_recipe(user_id, recipe_id)
    if not recipe:
        return
    text = recipe_detail_screen(recipe, recipe.get("match"))
    safe_edit(
        bot, chat_id, message_id, text,
        recipe_detail_keyboard(recipe_id, recipe.get("is_favorite", False)),
    )


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
                nav_service.replace(user_id, "recipe_detail", {"recipe_id": recipe_id})
                show_recipe(bot, chat_id, msg_id, user_id, recipe_id)

            elif action == "ingredients":
                answer_callback(bot, call)
                recipe_id = int(parts[2])
                recipe = recipe_service.get_recipe_detail(recipe_id, user_id)
                if not recipe:
                    return
                from services.ingredient_service import IngredientService
                combined = IngredientService().get_combined_ids(user_id)

                lines = []
                for ri in recipe.get("ingredients", []):
                    mark = "✅" if ri["ingredient_id"] in combined else "❌"
                    amount = f" — {ri['amount']} {ri['unit']}" if ri.get("amount") else ""
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
                recipe = recipe_service.get_recipe(recipe_id)
                if not recipe:
                    return
                desc = recipe.get("description") or "دستور پخت به زودی اضافه می‌شود."
                total_time = recipe.get("prep_time", 0) + recipe.get("cook_time", 0)
                text = build_screen(
                    emoji="👨‍🍳",
                    title=f"دستور پخت — {recipe['name']}",
                    description=f"⏱  زمان تقریبی: <b>{total_time}</b> دقیقه",
                    body=esc(desc),
                    footer=ACTION_FOOTER,
                    escape_title=False,
                )
                safe_edit(bot, chat_id, msg_id, text, recipe_sub_keyboard(recipe_id))

            elif action == "missing":
                answer_callback(bot, call)
                recipe_id = int(parts[2])
                recipe = recipe_service.get_recipe_detail(recipe_id, user_id)
                if not recipe or not recipe.get("match"):
                    return
                missing = recipe["match"].missing_ingredients
                if not missing:
                    body = "🎉  همه مواد لازم رو داری!\nمی‌تونی همین الان شروع به پخت کنی."
                else:
                    lines = [f"❌  {m['emoji']} {esc(m['name'])}" for m in missing]
                    body = list_body(lines)
                text = build_screen(
                    emoji="🛒",
                    title="چیزایی که ندارم",
                    description=f"برای «{esc(recipe['name'])}» این مواد کم داری:",
                    body=body,
                    footer=ACTION_FOOTER,
                    escape_title=False,
                )
                safe_edit(bot, chat_id, msg_id, text, recipe_sub_keyboard(recipe_id))

            elif action == "similar":
                answer_callback(bot, call)
                recipe_id = int(parts[2])
                nav_service.push_current(user_id)
                similar = recipe_service.get_similar(recipe_id)
                if not similar:
                    text = build_screen(
                        emoji="🔄",
                        title="غذاهای مشابه",
                        description="غذای مشابهی پیدا نشد.",
                        footer=ACTION_FOOTER,
                    )
                    safe_edit(bot, chat_id, msg_id, text, recipe_sub_keyboard(recipe_id))
                else:
                    nav_service.set_current(user_id, "recipe_similar", {"recipe_id": recipe_id})
                    text = build_screen(
                        emoji="🔄",
                        title="غذاهای مشابه",
                        description="این غذاها به غذای انتخابی شما نزدیک‌ترن:",
                        details=[f"📋  {len(similar)} پیشنهاد"],
                        footer="👇 روی غذا بزن",
                    )
                    safe_edit(bot, chat_id, msg_id, text, recipe_list_keyboard(similar))

            elif action == "share":
                answer_callback(bot, call)
                recipe_id = int(parts[2])
                recipe = recipe_service.get_recipe(recipe_id)
                if recipe:
                    share_text = f"🍲 {recipe['name']}\n\nبا ربات «غذا چی بپزم؟» پیداش کردم!"
                    try:
                        bot.answer_callback_query(call.id, share_text, show_alert=True)
                    except Exception:
                        pass
            else:
                answer_callback(bot, call)

        except Exception as e:
            from utils.logger import setup_logger
            setup_logger(__name__).exception("recipe handler error: %s", e)
            answer_callback(bot, call)
            show_error(bot, call, "nav:home")

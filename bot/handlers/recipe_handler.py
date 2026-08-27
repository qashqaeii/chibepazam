from telebot import TeleBot

from bot.handlers.base import safe_edit, answer_callback, show_error
from bot.keyboards.recipe import recipe_detail_keyboard, recipe_list_keyboard
from telebot import types
from services.recipe_service import RecipeService
from services.user_service import UserService
from services.nav_service import nav_service
from utils.telegram import esc, difficulty_label, cost_label


recipe_service = RecipeService()
user_service = UserService()


def show_recipe(bot: TeleBot, chat_id: int, message_id: int, user_id: int, recipe_id: int) -> None:
    recipe = recipe_service.view_recipe(user_id, recipe_id)
    if not recipe:
        return

    match = recipe.get("match")
    total_time = recipe_service.format_cook_time(recipe)
    text = (
        f"{recipe.get('emoji', '🍲')} <b>{esc(recipe['name'])}</b>\n\n"
        f"⭐ امتیاز: {recipe.get('rating', 4.0)}\n"
        f"⏱ زمان تقریبی: {total_time} دقیقه\n"
        f"👨‍🍳 سختی: {difficulty_label(recipe.get('difficulty', 'medium'))}\n"
        f"💰 هزینه: {cost_label(recipe.get('cost_level', 'medium'))}\n"
        f"👨‍👩‍👧‍👦 مناسب {recipe.get('servings', 4)} نفر\n\n"
    )
    if match:
        text += (
            f"🧺 تطابق با مواد شما: <b>{match.score:.0f}٪</b>\n\n"
            f"✅ {match.have_count} ماده رو داری\n"
            f"❌ {match.missing_count} ماده کم داری"
        )

    safe_edit(
        bot,
        chat_id,
        message_id,
        text,
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
                    cur
                    and cur["screen"] == "recipe_detail"
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
                    lines.append(f"{mark} {ri['emoji']} {esc(ri['name'])}{amount}")

                text = f"🥕 <b>مواد لازم — {esc(recipe['name'])}</b>\n\n" + "\n".join(lines)
                kb = types.InlineKeyboardMarkup()
                kb.add(types.InlineKeyboardButton("⬅️ بازگشت", callback_data=f"recipe:view:{recipe_id}:b"))
                safe_edit(bot, chat_id, msg_id, text, kb)

            elif action == "steps":
                answer_callback(bot, call)
                recipe_id = int(parts[2])
                recipe = recipe_service.get_recipe(recipe_id)
                if not recipe:
                    return
                desc = recipe.get("description") or "دستور پخت به زودی اضافه می‌شود."
                text = f"👨‍🍳 <b>دستور پخت — {esc(recipe['name'])}</b>\n\n{esc(desc)}"
                kb = types.InlineKeyboardMarkup()
                kb.add(types.InlineKeyboardButton("⬅️ بازگشت", callback_data=f"recipe:view:{recipe_id}:b"))
                safe_edit(bot, chat_id, msg_id, text, kb)

            elif action == "missing":
                answer_callback(bot, call)
                recipe_id = int(parts[2])
                recipe = recipe_service.get_recipe_detail(recipe_id, user_id)
                if not recipe or not recipe.get("match"):
                    return
                missing = recipe["match"].missing_ingredients
                if not missing:
                    text = "🛒 همه مواد لازم رو داری! ✅"
                else:
                    lines = "\n".join(f"❌ {m['emoji']} {esc(m['name'])}" for m in missing)
                    text = f"🛒 <b>چیزایی که ندارم</b>\n\n{lines}"
                kb = types.InlineKeyboardMarkup()
                kb.add(types.InlineKeyboardButton("⬅️ بازگشت", callback_data=f"recipe:view:{recipe_id}:b"))
                safe_edit(bot, chat_id, msg_id, text, kb)

            elif action == "similar":
                answer_callback(bot, call)
                recipe_id = int(parts[2])
                nav_service.push_current(user_id)
                similar = recipe_service.get_similar(recipe_id)
                if not similar:
                    text = "🔄 غذای مشابهی پیدا نشد."
                    kb = types.InlineKeyboardMarkup()
                    kb.add(types.InlineKeyboardButton("⬅️ بازگشت", callback_data=f"recipe:view:{recipe_id}:b"))
                else:
                    nav_service.set_current(user_id, "recipe_similar", {"recipe_id": recipe_id})
                    text = "🔄 <b>غذاهای مشابه</b>"
                    kb = recipe_list_keyboard(similar)
                safe_edit(bot, chat_id, msg_id, text, kb)

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

from telebot import TeleBot, types

from bot.handlers.base import safe_edit, answer_callback
from bot.keyboards.builder import btn, append_nav
from bot.keyboards.recipe import recipe_list_keyboard
from services.decision_service import DecisionService
from services.user_service import UserService
from services.nav_service import nav_service
from utils.screen import build_screen, ACTION_FOOTER


decision_service = DecisionService()
user_service = UserService()


def _kb(rows: list[list[tuple[str, str]]]) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    for row in rows:
        kb.row(*[btn(label, cb) for label, cb in row])
    return append_nav(kb)


def show_decision_start(bot: TeleBot, chat_id: int, message_id: int, user_id: int) -> None:
    nav_service.navigate(user_id, "decision_flow", {"step": "time", "filters": {}})
    text = build_screen(
        emoji="🤔",
        title="نمی‌دونم چی می‌خوام",
        description="چند سؤال کوتاه — بعد بهترین پیشنهادها رو می‌دم.",
        footer="👇 چقدر وقت داری؟",
    )
    safe_edit(bot, chat_id, message_id, text, _kb([
        [("⚡ کمتر از ۱ ساعت", "decide:time:60"), ("⏳ ۱ تا ۲ ساعت", "decide:time:120")],
        [("🕐 هر مدت", "decide:time:0")],
    ]))


def register_decision_handlers(bot: TeleBot) -> None:
    @bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("decide:"))
    def handle_decide(call):
        answer_callback(bot, call)
        user = user_service.get_user(call.from_user.id)
        if not user:
            return
        uid = user["id"]
        chat_id = call.message.chat.id
        msg_id = call.message.message_id
        parts = call.data.split(":")
        step = parts[1]
        val = parts[2] if len(parts) > 2 else ""
        cur = nav_service.get_current(uid) or {"payload": {"filters": {}}}
        filters = dict(cur.get("payload", {}).get("filters") or {})

        if step == "time":
            if val != "0":
                filters["max_time"] = int(val)
            nav_service.replace(uid, "decision_flow", {"step": "meal", "filters": filters})
            text = build_screen(emoji="🍽", title="نوع غذا", description="چه نوع غذایی دوست داری؟", footer="👇 انتخاب کن")
            safe_edit(bot, chat_id, msg_id, text, _kb([
                [("🍚 پلو", "decide:meal:polo"), ("🥘 خورش", "decide:meal:stew")],
                [("🍖 کباب", "decide:meal:kebab"), ("🥣 آش", "decide:meal:ash")],
                [("🎲 هر نوع", "decide:meal:any")],
            ]))
        elif step == "meal":
            meal_map = {"polo": ["polo"], "stew": ["stew", "traditional"], "kebab": ["kebab"], "ash": ["ash"]}
            if val != "any":
                filters["category_slugs"] = meal_map.get(val, [])
            nav_service.replace(uid, "decision_flow", {"step": "protein", "filters": filters})
            text = build_screen(emoji="🥩", title="پروتئین", description="ترجیح پروتئین؟", footer="👇 انتخاب کن")
            safe_edit(bot, chat_id, msg_id, text, _kb([
                [("🍗 مرغ", "decide:protein:chicken"), ("🥩 گوشت", "decide:protein:meat")],
                [("🐟 ماهی", "decide:protein:fish"), ("🌱 گیاهی", "decide:protein:veg")],
                [("🎲 مهم نیست", "decide:protein:any")],
            ]))
        elif step == "protein":
            if val == "veg":
                filters["vegetarian"] = True
            elif val != "any":
                filters["protein"] = val
            nav_service.replace(uid, "decision_flow", {"step": "cost", "filters": filters})
            text = build_screen(emoji="💰", title="بودجه", description="سطح هزینه؟", footer="👇 انتخاب کن")
            safe_edit(bot, chat_id, msg_id, text, _kb([
                [("💚 اقتصادی", "decide:cost:low"), ("💛 متوسط", "decide:cost:medium")],
                [("💎 بالاتر", "decide:cost:high"), ("🎲 مهم نیست", "decide:cost:any")],
            ]))
        elif step == "cost":
            if val != "any":
                filters["cost_level"] = val
            recipes = decision_service.resolve(filters, uid, limit=5)
            nav_service.replace(uid, "decision_flow", {"step": "result", "filters": filters})
            if not recipes:
                text = build_screen(emoji="😕", title="نتیجه", description="غذای مناسبی پیدا نشد. فیلترها را تغییر بده.", footer=ACTION_FOOTER)
                safe_edit(bot, chat_id, msg_id, text, append_nav(types.InlineKeyboardMarkup()))
            else:
                text = build_screen(
                    emoji="✨", title="پیشنهاد برای تو",
                    description="بر اساس انتخاب‌هایت:", details=[f"📋  {len(recipes)} غذا"],
                    footer="👇 روی غذا بزن",
                )
                safe_edit(bot, chat_id, msg_id, text, recipe_list_keyboard(recipes))

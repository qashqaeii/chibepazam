from telebot import TeleBot, types

from bot.handlers.base import safe_edit, answer_callback
from bot.keyboards.builder import btn, append_nav
from bot.keyboards.recipe import recipe_list_keyboard
from services.decision_service import DecisionService
from services.user_service import UserService
from services.nav_service import nav_service
from utils.screen import build_screen, ACTION_FOOTER
from utils.menu_style import step_line, section, join_sections


decision_service = DecisionService()
user_service = UserService()

STEPS = {
    "time": (1, "چقدر وقت برای پخت داری؟"),
    "meal": (2, "چه نوع غذایی دوست داری؟"),
    "protein": (3, "پروتئین مورد علاقه‌ات چیه؟"),
    "cost": (4, "بودجه تقریبی چقدره؟"),
}


def _kb(rows: list[list[tuple[str, str]]]) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    for row in rows:
        kb.row(*[btn(label, cb) for label, cb in row])
    return append_nav(kb)


def _step_screen(emoji: str, title: str, step_key: str, hint: str, body: str | None = None) -> str:
    num, _ = STEPS[step_key]
    return build_screen(
        emoji=emoji,
        title=title,
        description=[
            step_line(num, 4),
            hint,
        ],
        body=body,
        footer=f"👇 {STEPS[step_key][1]}",
    )


def show_decision_start(bot: TeleBot, chat_id: int, message_id: int, user_id: int) -> None:
    nav_service.navigate(user_id, "decision_flow", {"step": "time", "filters": {}})
    text = _step_screen(
        "🤔", "نمی‌دونم چی می‌خوام", "time",
        "چند سؤال کوتاه می‌پرسم تا بهترین پیشنهاد را بدهم.",
        section("راهنما", [
            "زمان → نوع غذا → پروتئین → بودجه",
            "در پایان ۵ پیشنهاد متناسب می‌بینی",
        ]),
    )
    safe_edit(bot, chat_id, message_id, text, _kb([
        [("⚡  زیر ۱ ساعت", "decide:time:60"), ("⏳  ۱ تا ۲ ساعت", "decide:time:120")],
        [("🕐  فرقی نداره", "decide:time:0")],
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
            text = _step_screen("🍽", "نوع غذا", "meal", "دسته غذایی مورد علاقه را انتخاب کن.")
            safe_edit(bot, chat_id, msg_id, text, _kb([
                [("🍚  پلو", "decide:meal:polo"), ("🥘  خورش", "decide:meal:stew")],
                [("🍖  کباب", "decide:meal:kebab"), ("🥣  آش", "decide:meal:ash")],
                [("🎲  هر نوعی", "decide:meal:any")],
            ]))
        elif step == "meal":
            meal_map = {"polo": ["polo"], "stew": ["stew", "traditional"], "kebab": ["kebab"], "ash": ["ash"]}
            if val != "any":
                filters["category_slugs"] = meal_map.get(val, [])
            nav_service.replace(uid, "decision_flow", {"step": "protein", "filters": filters})
            text = _step_screen("🥩", "نوع پروتئین", "protein", "ترجیح پروتئین را مشخص کن.")
            safe_edit(bot, chat_id, msg_id, text, _kb([
                [("🍗  مرغ", "decide:protein:chicken"), ("🥩  گوشت", "decide:protein:meat")],
                [("🐟  ماهی", "decide:protein:fish"), ("🌱  گیاهی", "decide:protein:veg")],
                [("🎲  مهم نیست", "decide:protein:any")],
            ]))
        elif step == "protein":
            if val == "veg":
                filters["vegetarian"] = True
            elif val != "any":
                filters["protein"] = val
            nav_service.replace(uid, "decision_flow", {"step": "cost", "filters": filters})
            text = _step_screen("💰", "بودجه", "cost", "سطح هزینه تقریبی را انتخاب کن.")
            safe_edit(bot, chat_id, msg_id, text, _kb([
                [("💚  اقتصادی", "decide:cost:low"), ("💛  متوسط", "decide:cost:medium")],
                [("💎  بالاتر", "decide:cost:high"), ("🎲  مهم نیست", "decide:cost:any")],
            ]))
        elif step == "cost":
            if val != "any":
                filters["cost_level"] = val
            recipes = decision_service.resolve(filters, uid, limit=5)
            nav_service.replace(uid, "decision_flow", {"step": "result", "filters": filters})
            if not recipes:
                text = build_screen(
                    emoji="😕",
                    title="نتیجه‌ای پیدا نشد",
                    description=[
                        "با این ترکیب انتخاب‌ها غذای مناسبی نبود.",
                        "از منوی اصلی «با مواد خونه» یا «پیشنهاد شانسی» امتحان کن.",
                    ],
                    footer=ACTION_FOOTER,
                )
                safe_edit(bot, chat_id, msg_id, text, append_nav(types.InlineKeyboardMarkup()))
            else:
                summary = section("خلاصه انتخاب‌ها", [
                    f"⏱  زمان: {'هر مدت' if not filters.get('max_time') else str(filters['max_time']) + ' دقیقه'}",
                    f"💰  بودجه: {filters.get('cost_level', 'مهم نیست')}",
                    f"🌱  گیاهی: {'بله' if filters.get('vegetarian') else 'خیر'}",
                ])
                text = build_screen(
                    emoji="✨",
                    title="پیشنهاد ویژه برای تو",
                    description=[
                        step_line(4, 4),
                        f"بر اساس انتخاب‌هایت، <b>{len(recipes)}</b> غذا پیدا شد:",
                    ],
                    body=summary,
                    footer="👇 روی غذا بزن برای جزئیات",
                )
                safe_edit(bot, chat_id, msg_id, text, recipe_list_keyboard(recipes))

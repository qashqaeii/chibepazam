"""Standard screen/message builder for consistent bot UI."""

from utils.telegram import esc

SEPARATOR = "─────────────────"
DEFAULT_FOOTER = "👇 یکی از گزینه‌ها رو انتخاب کن"
ACTION_FOOTER = "👇 عملیات مورد نظر رو انتخاب کن"
NAV_FOOTER = "👇 برای بازگشت از دکمه‌های پایین استفاده کن"


def _lines(*parts: str | None) -> list[str]:
    return [p for p in parts if p]


def build_screen(
    emoji: str,
    title: str,
    description: str | list[str] | None = None,
    details: list[str] | None = None,
    body: str | None = None,
    footer: str | None = DEFAULT_FOOTER,
    escape_title: bool = True,
) -> str:
    """
    Build a standard menu message:
      {emoji} Bold Title
      description (max ~2 lines)
      ─────────
      details / body
      👇 footer
    """
    title_text = esc(title) if escape_title else title
    parts = [f"{emoji} <b>{title_text}</b>"]

    if description:
        if isinstance(description, list):
            parts.extend(description[:2])
        else:
            for line in description.split("\n")[:2]:
                if line.strip():
                    parts.append(line.strip())
        parts.append("")

    blocks: list[str] = []
    if details:
        blocks.append("\n".join(details))
    if body:
        blocks.append(body)

    if blocks:
        parts.append(SEPARATOR)
        parts.append("\n\n".join(blocks))

    if footer:
        parts.append("")
        parts.append(footer)

    return "\n".join(parts)


def recipe_detail_screen(recipe: dict, match=None) -> str:
    from utils.telegram import difficulty_label, cost_label

    name = esc(recipe.get("name", ""))
    emoji = recipe.get("emoji", "🍲")
    desc = recipe.get("description") or "یک غذای خوش‌طعم ایرانی"

    total_time = recipe.get("prep_time", 0) + recipe.get("cook_time", 0)
    rating = recipe.get("rating", 4.0)
    rating_count = recipe.get("rating_count", 0)
    rating_line = f"⭐ امتیاز: <b>{rating:.1f}</b>"
    if rating_count:
        rating_line += f"  ({rating_count} رأی)"
    display_servings = recipe.get("display_servings") or recipe.get("servings", 4)
    details = _lines(
        rating_line,
        f"⏱ زمان: <b>{total_time}</b> دقیقه",
        f"👨‍🍳 سختی: {difficulty_label(recipe.get('difficulty', 'medium'))}",
        f"💰 هزینه: {cost_label(recipe.get('cost_level', 'medium'))}",
        f"👨‍👩‍👧‍👦 مناسب: <b>{display_servings}</b> نفر",
    )

    body = None
    if match:
        body = (
            f"🧺 تطابق با مواد شما: <b>{match.score:.0f}٪</b>\n"
            f"✅ {match.have_count} ماده داری  ·  ❌ {match.missing_count} ماده کم داری"
        )

    # Title includes dish emoji + name inline
    parts = [
        f"{emoji} <b>{name}</b>",
        "",
        desc[:200] + ("…" if len(desc) > 200 else ""),
        "",
        SEPARATOR,
        "\n".join(details),
    ]
    if body:
        parts.extend(["", SEPARATOR, body])
    parts.extend(["", ACTION_FOOTER])
    return "\n".join(parts)


def recipe_card_screen(
    emoji: str,
    name: str,
    description: str,
    details: list[str],
    header_emoji: str = "🎲",
    header_title: str = "پیشنهاد من",
) -> str:
    return build_screen(
        emoji=header_emoji,
        title=header_title,
        description=[
            f"{emoji} <b>{esc(name)}</b>",
            description[:100] + ("…" if len(description) > 100 else ""),
        ],
        details=details,
        footer=ACTION_FOOTER,
        escape_title=False,
    )


def list_body(items: list[str], empty_text: str = "موردی یافت نشد.") -> str:
    if not items:
        return empty_text
    return "\n".join(items)

import html


def esc(text: str | None) -> str:
    """Escape HTML special characters for Telegram parse_mode=HTML."""
    if text is None:
        return ""
    return html.escape(str(text))


def difficulty_label(level: str) -> str:
    labels = {"easy": "آسان", "medium": "متوسط", "hard": "سخت"}
    return labels.get(level, level)


def cost_label(level: str) -> str:
    labels = {"low": "اقتصادی", "medium": "متوسط", "high": "گران"}
    return labels.get(level, level)


def match_emoji(score: float) -> str:
    if score >= 90:
        return "🔥"
    if score >= 70:
        return "🟢"
    if score >= 50:
        return "🟡"
    return "🔴"

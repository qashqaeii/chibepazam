"""Shared menu copy and layout helpers for consistent bot UI."""

from utils.screen import SEPARATOR

BULLET = "▪️"


def step_line(current: int, total: int) -> str:
    bar = "●" * current + "○" * (total - current)
    return f"📍 مرحله <b>{current}</b> از <b>{total}</b>  {bar}"


def section(title: str, lines: list[str]) -> str:
    if not lines:
        return ""
    body = "\n".join(f"{BULLET}  {line}" for line in lines)
    return f"<b>{title}</b>\n{body}"


def join_sections(*blocks: str) -> str:
    parts = [b for b in blocks if b.strip()]
    return f"\n\n{SEPARATOR}\n\n".join(parts)


def menu_hint(*lines: str) -> list[str]:
    return list(lines)


def status_chip(label: str, value: str | int, emoji: str = "📌") -> str:
    return f"{emoji}  {label}: <b>{value}</b>"

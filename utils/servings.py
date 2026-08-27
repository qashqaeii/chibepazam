"""Scale recipe ingredient amounts based on user servings."""

import re
from fractions import Fraction

_FA_TO_EN = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
_FRACTIONS = {"½": "0.5", "¼": "0.25", "¾": "0.75", "⅓": "0.333", "⅔": "0.667"}


def _normalize_number(text: str) -> str:
    t = text.translate(_FA_TO_EN).strip()
    for k, v in _FRACTIONS.items():
        t = t.replace(k, v)
    t = t.replace("،", ".").replace(",", ".")
    return t


def _format_number(value: float) -> str:
    if abs(value - round(value)) < 0.05:
        n = int(round(value))
        return str(n).translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹"))
    whole = int(value)
    frac = value - whole
    frac_map = {0.5: "½", 0.25: "¼", 0.75: "¾", 0.333: "⅓", 0.667: "⅔"}
    for f, sym in frac_map.items():
        if abs(frac - f) < 0.08:
            if whole:
                return f"{whole}{sym}"
            return sym
    rounded = round(value, 1)
    s = str(rounded).translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹"))
    return s.replace(".", "٫")


def scale_amount(amount: str | None, ratio: float) -> str | None:
    if not amount or ratio == 1.0:
        return amount
    raw = amount.strip()
    if not raw or raw in ("به اندازه نیاز", "برای سرخ کردن"):
        return amount

    range_m = re.match(r"^([\d½¼¾⅓⅔\.]+)\s*تا\s*([\d½¼¾⅓⅔\.]+)$", _normalize_number(raw))
    if range_m:
        lo = float(Fraction(range_m.group(1)))
        hi = float(Fraction(range_m.group(2)))
        return f"{_format_number(lo * ratio)} تا {_format_number(hi * ratio)}"

    parts = re.split(r"(\s+)", raw)
    out: list[str] = []
    for part in parts:
        if not part.strip():
            out.append(part)
            continue
        norm = _normalize_number(part)
        if re.match(r"^[\d\.]+$", norm):
            try:
                val = float(Fraction(norm)) * ratio
                out.append(_format_number(val))
                continue
            except (ValueError, ZeroDivisionError):
                pass
        out.append(part)
    return "".join(out) if out else amount


def scale_ingredient_row(row: dict, recipe_servings: int, target_servings: int) -> dict:
    if not target_servings or not recipe_servings or target_servings == recipe_servings:
        return dict(row)
    ratio = target_servings / recipe_servings
    scaled = dict(row)
    scaled["amount"] = scale_amount(row.get("amount"), ratio)
    scaled["base_amount"] = row.get("amount")
    scaled["scaled_servings"] = target_servings
    return scaled


def scale_ingredients(rows: list[dict], recipe_servings: int, target_servings: int) -> list[dict]:
    return [scale_ingredient_row(r, recipe_servings, target_servings) for r in rows]

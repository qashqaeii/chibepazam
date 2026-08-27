"""Foundation verification tests — run without Telegram bot."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from services.recipe_service import RecipeService


def test_match_score_bounds():
    svc = RecipeService()
    ingredients = [
        {"ingredient_id": 1, "importance": 10, "is_required": 1, "is_common": 0},
        {"ingredient_id": 2, "importance": 1, "is_required": 0, "is_common": 1},
    ]
    # all present
    m = svc._calculate_match(ingredients, {1, 2})
    assert 0 <= m.score <= 100, f"score out of bounds: {m.score}"
    assert m.score > 90

    # missing required high importance
    m2 = svc._calculate_match(ingredients, {2})
    assert 0 <= m2.score <= 100
    assert m2.missing_count == 1

    # empty ingredients
    m3 = svc._calculate_match([], {1})
    assert m3.score == 0


def test_optional_low_weight():
    svc = RecipeService()
    ingredients = [
        {"ingredient_id": 1, "importance": 10, "is_required": 1, "is_common": 0},
        {"ingredient_id": 2, "importance": 1, "is_required": 0, "is_common": 1},
    ]
    with_required = svc._calculate_match(ingredients, {1})
    without_salt = svc._calculate_match(ingredients, {1})
    assert with_required.score == without_salt.score


def test_nav_stack_logic():
    from services.nav_service import NavService, _current

    nav = NavService()
    uid = 999999

    nav.set_current(uid, "home", {})
    assert nav.get_current(uid)["screen"] == "home"

    nav.set_current(uid, "pantry_main", {})
    assert nav.get_current(uid)["screen"] == "pantry_main"

    _current.pop(uid, None)


def test_shopping_list_text():
    from utils.shopping import build_shopping_list, build_share_url, ingredient_qty

    recipe = {"name": "باقالی‌پلو با ماهیچه", "servings": 4}
    missing = [
        {"name": "ماهیچه", "emoji": "🥩", "amount": "۴", "unit": "عدد"},
        {"name": "برنج", "emoji": "🍚", "amount": "۳", "unit": "پیمانه"},
    ]
    text = build_shopping_list(recipe, missing)
    assert "باقالی‌پلو با ماهیچه" in text
    assert "ماهیچه" in text
    assert "۴ عدد" in text
    assert "۳ پیمانه" in text
    assert "۴ نفر" in text or "۴" in text
    assert ingredient_qty(missing[0]) == "۴ عدد"
    url = build_share_url(text, "chibepazam")
    if url:
        assert url.startswith("https://t.me/share/url?")
        assert len(url) <= 2000


def test_callback_data_length():
    samples = [
        "nav:home",
        "page:ing:2:3",
        "recipe:view:123:b",
        "page:rst:20:2",
        "recipe:buylist:20",
        "pantry:ingredient:163:10:5",
    ]
    for s in samples:
        assert len(s.encode("utf-8")) <= 64, f"callback too long: {s}"


if __name__ == "__main__":
    test_match_score_bounds()
    test_optional_low_weight()
    test_nav_stack_logic()
    test_shopping_list_text()
    test_callback_data_length()
    print("All foundation checks passed.")

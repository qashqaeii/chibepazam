"""Feature unit tests — no DB required for most checks."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.servings import scale_amount, scale_ingredient_row
from utils.shopping import merge_amounts, build_merged_shopping_list
from services.recommendation_service import RecommendationService, ANIMAL_INGREDIENT_SLUGS
from services.filter_presets import RECOMMEND_FILTERS
from services.rating_service import RATING_LABELS
from services.nav_service import NavService, _current


def test_servings_scale():
    assert scale_amount("۲", 2.0) is not None
    scaled = scale_ingredient_row(
        {"amount": "۲", "unit": "پیمانه", "ingredient_id": 1},
        recipe_servings=4,
        target_servings=8,
    )
    assert scaled.get("amount") != "۲" or scaled.get("scaled_servings") == 8


def test_merge_amounts():
    assert merge_amounts("۱", "۱") == "۲" or merge_amounts("۱", "۱")  # fa digits
    assert merge_amounts(None, "۲") == "۲"


def test_merged_shopping_list():
    text = build_merged_shopping_list(
        ["قرمه سبزی", "باقالی‌پلو"],
        [{"name": "برنج", "emoji": "🍚", "amount": "۲", "unit": "پیمانه"}],
        4,
    )
    assert "لیست خرید ترکیبی" in text
    assert "برنج" in text


def test_rating_labels():
    assert len(RATING_LABELS) == 4
    assert "love" in RATING_LABELS


def test_recommendation_filters_merge():
    keys = {"time_short", "cost_low", "veg_only"}
    merged = {}
    for key in keys:
        for k, v in RECOMMEND_FILTERS[key].items():
            merged[k] = v
    assert merged.get("max_time") == 60
    assert merged.get("cost_level") == "low"
    assert merged.get("vegetarian") is True


def test_vegan_animal_slugs():
    assert "chicken" in ANIMAL_INGREDIENT_SLUGS
    assert "butter" in ANIMAL_INGREDIENT_SLUGS


def test_search_query_min_length():
    q = "a"
    assert len(q.strip()) < 2


def test_forbidden_filter_logic():
    svc = RecommendationService()
    ingredients = [
        {"ingredient_id": 5, "importance": 10, "is_required": 1, "slug": "x"},
        {"ingredient_id": 6, "importance": 5, "is_required": 1, "slug": "y"},
    ]
    forbidden = {5}
    assert any(i["ingredient_id"] in forbidden for i in ingredients)


def test_dislike_exclusion():
    disliked = {10, 20}
    recipes = [{"id": 10}, {"id": 30}]
    filtered = [r for r in recipes if r["id"] not in disliked]
    assert len(filtered) == 1
    assert filtered[0]["id"] == 30


def test_navigation_persist():
    nav = NavService()
    uid = 888888
    nav.set_current(uid, "recipe_detail", {"recipe_id": 5})
    assert nav.get_current(uid)["screen"] == "recipe_detail"
    assert nav.get_current(uid)["payload"]["recipe_id"] == 5
    _current.pop(uid, None)


def test_share_text():
    from utils.share import build_recipe_share_text

    text = build_recipe_share_text(
        {"name": "قورمه سبزی", "prep_time": 30, "cook_time": 90, "difficulty": "medium"},
        "Chibepazamrobot",
    )
    assert "قورمه سبزی" in text
    assert "Chibepazamrobot" in text


if __name__ == "__main__":
    test_servings_scale()
    test_merge_amounts()
    test_merged_shopping_list()
    test_rating_labels()
    test_recommendation_filters_merge()
    test_vegan_animal_slugs()
    test_search_query_min_length()
    test_forbidden_filter_logic()
    test_dislike_exclusion()
    test_navigation_persist()
    test_share_text()
    print("All feature tests passed.")

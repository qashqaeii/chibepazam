"""Validate seed data without requiring a live MySQL connection."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database.seed_data import INGREDIENTS, INGREDIENT_CATEGORIES, RECIPE_CATEGORIES, RECIPES


def test_seed_integrity():
    ing_ids = {i[0] for i in INGREDIENTS}
    ing_slugs = [i[3] for i in INGREDIENTS]
    cat_ids = {c[0] for c in INGREDIENT_CATEGORIES}
    rcat_ids = {c[0] for c in RECIPE_CATEGORIES}

    assert len(INGREDIENTS) == len(ing_ids)
    assert len(ing_slugs) == len(set(ing_slugs))
    assert len(RECIPES) == 20
    assert len({r["id"] for r in RECIPES}) == 20
    assert len({r["slug"] for r in RECIPES}) == 20
    assert len(INGREDIENT_CATEGORIES) == 10
    assert len(RECIPE_CATEGORIES) == 6

    for item in INGREDIENTS:
        assert item[1] in cat_ids, item

    for recipe in RECIPES:
        assert recipe["category_id"] in rcat_ids, recipe["slug"]
        assert recipe.get("instructions")
        assert recipe.get("description")
        assert recipe.get("ingredients")
        assert recipe["cook_time"] > 0
        seen = set()
        required = 0
        for row in recipe["ingredients"]:
            iid = row["ingredient_id"]
            assert iid not in seen, (recipe["slug"], iid)
            seen.add(iid)
            assert iid in ing_ids, (recipe["slug"], iid)
            if row["is_required"]:
                required += 1
        assert required > 0, recipe["slug"]


if __name__ == "__main__":
    test_seed_integrity()
    links = sum(len(r["ingredients"]) for r in RECIPES)
    vegetarian = [r["name"] for r in RECIPES if r["is_vegetarian"]]
    print(f"recipes={len(RECIPES)} ingredients={len(INGREDIENTS)} links={links}")
    print("vegetarian_count=", len(vegetarian))
    print("Seed data integrity checks passed.")

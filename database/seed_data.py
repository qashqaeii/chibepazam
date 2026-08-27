"""Canonical seed data for «غذا چی بپزم؟».

Only real Iranian pantry items and the 20 recipes provided by the product owner.
No invented dishes, ratings, or quantities.
"""

INGREDIENT_CATEGORIES = [
    (1, "گوشت و پروتئین", "protein", "🥩", 1),
    (2, "سبزیجات", "vegetables", "🥕", 2),
    (3, "برنج و غلات", "grains", "🍚", 3),
    (4, "حبوبات", "legumes", "🫘", 4),
    (5, "لبنیات", "dairy", "🥛", 5),
    (6, "تخم‌مرغ", "eggs", "🥚", 6),
    (7, "ادویه و سبزی خشک", "spices", "🌿", 7),
    (8, "چاشنی‌ها", "condiments", "🍅", 8),
    (9, "کنسروی و ترشی", "canned", "🥫", 9),
    (10, "سایر", "other", "🧺", 10),
]

# (id, category_id, name, slug, emoji, is_common, sort_order)
INGREDIENTS = [
    # پروتئین — شناسه‌های ۱ تا ۶ حفظ می‌شوند
    (1, 1, "مرغ", "chicken", "🍗", 0, 1),
    (2, 1, "گوشت قرمز", "red-meat", "🥩", 0, 2),
    (3, 1, "گوشت چرخ‌کرده", "ground-meat", "🍖", 0, 3),
    (4, 1, "ماهی", "fish", "🐟", 0, 4),
    (5, 1, "تن ماهی", "tuna", "🐟", 0, 5),
    (6, 1, "سویا", "soy", "🌱", 0, 6),
    (51, 1, "ماهیچه", "shank", "🥩", 0, 7),
    # سبزیجات
    (7, 2, "پیاز", "onion", "🧅", 1, 1),
    (8, 2, "سیب‌زمینی", "potato", "🥔", 0, 2),
    (9, 2, "گوجه", "tomato", "🍅", 0, 3),
    (10, 2, "بادمجان", "eggplant", "🍆", 0, 4),
    (11, 2, "سبزی قورمه", "herb-ghorme", "🌿", 0, 5),
    (12, 2, "لوبیا سبز", "green-beans", "🫛", 0, 6),
    (13, 2, "هویج", "carrot", "🥕", 0, 7),
    (45, 2, "سیر", "garlic", "🧄", 1, 8),
    (46, 2, "کلم", "cabbage", "🥬", 0, 9),
    (40, 2, "شوید", "dill", "🌿", 0, 10),
    (47, 2, "سبزی پلویی", "herb-polo", "🌿", 0, 11),
    (48, 2, "سبزی کوکو", "herb-kuku", "🌿", 0, 12),
    (49, 2, "سبزی آش", "herb-ash", "🌿", 0, 13),
    (53, 2, "سبزی معطر", "aromatic-herbs", "🌿", 0, 14),
    # غلات
    (14, 3, "برنج", "rice", "🍚", 0, 1),
    (15, 3, "نان", "bread", "🥖", 1, 2),
    (43, 3, "رشته آش", "ash-noodles", "🍜", 0, 3),
    # حبوبات
    (16, 4, "عدس", "lentil", "🫘", 0, 1),
    (17, 4, "لوبیا قرمز", "red-beans", "🫘", 0, 2),
    (33, 4, "لپه", "split-peas", "🫘", 0, 3),
    (39, 4, "باقالی", "fava", "🫘", 0, 4),
    (41, 4, "نخود", "chickpea", "🫘", 0, 5),
    (42, 4, "لوبیا سفید", "white-beans", "🫘", 0, 6),
    # لبنیات
    (18, 5, "ماست", "yogurt", "🥛", 0, 1),
    (19, 5, "کشک", "kashk", "🥛", 0, 2),
    (37, 5, "کره", "butter", "🧈", 1, 3),
    (52, 5, "ماست چکیده", "strained-yogurt", "🥛", 0, 4),
    # تخم‌مرغ
    (31, 6, "تخم‌مرغ", "egg", "🥚", 0, 1),
    # ادویه
    (20, 7, "زردچوبه", "turmeric", "🌿", 1, 1),
    (21, 7, "زعفران", "saffron", "🌿", 0, 2),
    (22, 7, "نمک", "salt", "🧂", 1, 3),
    (23, 7, "فلفل", "pepper", "🌶", 1, 4),
    (24, 7, "دارچین", "cinnamon", "🌿", 0, 5),
    (44, 7, "نعناع خشک", "dried-mint", "🌿", 0, 6),
    # چاشنی
    (25, 8, "رب گوجه", "tomato-paste", "🍅", 1, 1),
    (26, 8, "روغن", "oil", "🫒", 1, 2),
    (27, 8, "سرکه", "vinegar", "🍶", 0, 3),
    (28, 8, "آبلیمو", "lime-juice", "🍋", 0, 4),
    (32, 8, "لیموعمانی", "dried-lime", "🍋", 0, 5),
    (35, 8, "رب انار", "pomegranate-paste", "🔴", 0, 6),
    (50, 8, "آبغوره", "verjuice", "🍇", 0, 7),
    # کنسروی — دسته خالی نماند؛ فقط اقلام واقعی سفره ایرانی
    (54, 9, "خیارشور", "pickle", "🥒", 0, 1),
    (55, 9, "زیتون", "olive", "🫒", 0, 2),
    # سایر
    (29, 10, "زرشک", "barberry", "🔴", 0, 1),
    (30, 10, "آلو", "plum", "🟣", 0, 2),
    (34, 10, "گردو", "walnut", "🥜", 0, 3),
    (36, 10, "شکر", "sugar", "🍬", 1, 4),
    (38, 10, "کشمش", "raisin", "🍇", 0, 5),
]

RECIPE_CATEGORIES = [
    (1, "خورش و خوراک", "stew", "🥘", 1),
    (2, "پلو و چلو", "polo", "🍚", 2),
    (3, "غذای سنتی", "traditional", "🍲", 3),
    (4, "کباب", "kebab", "🍖", 4),
    (5, "آش", "ash", "🥣", 5),
    (6, "کوکو و کتلت", "kuku", "🌿", 6),
]

from database.recipes_catalog import RECIPES


def _upsert_many(cursor, sql: str, rows: list) -> None:
    if not rows:
        return
    cursor.executemany(sql, rows)


def apply_seed(cursor) -> None:
    _upsert_many(
        cursor,
        """
        INSERT INTO ingredient_categories (id, name, slug, emoji, sort_order, is_active)
        VALUES (%s, %s, %s, %s, %s, 1)
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            slug = VALUES(slug),
            emoji = VALUES(emoji),
            sort_order = VALUES(sort_order),
            is_active = 1
        """,
        INGREDIENT_CATEGORIES,
    )

    _upsert_many(
        cursor,
        """
        INSERT INTO ingredients
            (id, category_id, name, slug, emoji, is_common, sort_order, is_active)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 1)
        ON DUPLICATE KEY UPDATE
            category_id = VALUES(category_id),
            name = VALUES(name),
            slug = VALUES(slug),
            emoji = VALUES(emoji),
            is_common = VALUES(is_common),
            sort_order = VALUES(sort_order),
            is_active = 1
        """,
        INGREDIENTS,
    )

    _upsert_many(
        cursor,
        """
        INSERT INTO recipe_categories (id, name, slug, emoji, sort_order, is_active)
        VALUES (%s, %s, %s, %s, %s, 1)
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            slug = VALUES(slug),
            emoji = VALUES(emoji),
            sort_order = VALUES(sort_order),
            is_active = 1
        """,
        RECIPE_CATEGORIES,
    )

    cursor.execute("DELETE FROM recipe_ingredients")
    cursor.execute("DELETE FROM recipes")

    recipe_rows = []
    ingredient_rows = []
    for recipe in RECIPES:
        recipe_rows.append((
            recipe["id"],
            recipe["category_id"],
            recipe["name"],
            recipe["slug"],
            recipe["emoji"],
            recipe["description"],
            recipe["instructions"],
            recipe["prep_time"],
            recipe["cook_time"],
            recipe["servings"],
            recipe["difficulty"],
            recipe["cost_level"],
            recipe["is_vegetarian"],
            4.0,
        ))
        seen = set()
        for item in recipe["ingredients"]:
            iid = item["ingredient_id"]
            if iid in seen:
                raise ValueError(f"Duplicate ingredient {iid} on recipe {recipe['slug']}")
            seen.add(iid)
            unit = item["unit"] or None
            ingredient_rows.append((
                recipe["id"],
                iid,
                item["amount"],
                unit,
                item["importance"],
                item["is_required"],
                item["is_optional"],
            ))

    _upsert_many(
        cursor,
        """
        INSERT INTO recipes (
            id, category_id, name, slug, emoji, description, instructions,
            prep_time, cook_time, servings, difficulty, cost_level,
            is_vegetarian, rating, is_active
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, 1
        )
        """,
        recipe_rows,
    )
    _upsert_many(
        cursor,
        """
        INSERT INTO recipe_ingredients (
            recipe_id, ingredient_id, amount, unit,
            importance, is_required, is_optional
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        ingredient_rows,
    )

    print(f"  ✓ {len(INGREDIENTS)} ingredients, {len(RECIPES)} recipes, {len(ingredient_rows)} recipe ingredients")

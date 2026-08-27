"""Canonical seed data for «غذا چی بپزم؟».

Real Iranian pantry items and a 100-recipe home-cooking catalog.
Quantities and steps are authentic household measures, not placeholders.
"""

INGREDIENT_CATEGORIES = [
    (1, "گوشت و پروتئین", "protein", "🥩", 1),
    (2, "سبزیجات", "vegetables", "🥕", 2),
    (3, "غلات و نان", "grains", "🍚", 3),
    (4, "حبوبات", "legumes", "🫘", 4),
    (5, "لبنیات", "dairy", "🥛", 5),
    (6, "سبزی تازه", "fresh-herbs", "🌿", 6),
    (7, "ادویه‌ها", "spices", "🧂", 7),
    (8, "چاشنی و روغن", "condiments", "🍅", 8),
    (9, "کنسرو و ترشی", "canned", "🥫", 9),
    (10, "خشکبار و میوه", "dry-fruit", "🥜", 10),
]

# شناسه‌های قبلی حفظ می‌شوند تا دستور غذاها و انتخاب کاربران نشکند.
# (id, category_id, name, slug, emoji, is_common, sort_order)
INGREDIENTS = [
    # ── گوشت و پروتئین ────────────────────────────────────
    (1, 1, "مرغ", "chicken", "🍗", 0, 1),
    (3, 1, "گوشت چرخ‌کرده", "ground-meat", "🍖", 0, 2),
    (2, 1, "گوشت قرمز", "red-meat", "🥩", 0, 3),
    (51, 1, "ماهیچه", "shank", "🥩", 0, 4),
    (4, 1, "ماهی", "fish", "🐟", 0, 5),
    (5, 1, "تن ماهی", "tuna", "🐟", 0, 6),
    (56, 1, "میگو", "shrimp", "🦐", 0, 7),
    (60, 1, "مرغ چرخ‌کرده", "ground-chicken", "🍗", 0, 8),
    (6, 1, "سویا", "soy", "🌱", 0, 9),
    (59, 1, "جگر", "liver", "🥩", 0, 10),
    (57, 1, "سوسیس", "sausage", "🌭", 0, 11),
    (58, 1, "کالباس", "mortadella", "🥓", 0, 12),
    # ── سبزیجات ───────────────────────────────────────────
    (7, 2, "پیاز", "onion", "🧅", 1, 1),
    (45, 2, "سیر", "garlic", "🧄", 1, 2),
    (8, 2, "سیب‌زمینی", "potato", "🥔", 0, 3),
    (9, 2, "گوجه‌فرنگی", "tomato", "🍅", 0, 4),
    (13, 2, "هویج", "carrot", "🥕", 0, 5),
    (65, 2, "خیار", "cucumber", "🥒", 0, 6),
    (61, 2, "فلفل دلمه‌ای", "bell-pepper", "🫑", 0, 7),
    (10, 2, "بادمجان", "eggplant", "🍆", 0, 8),
    (12, 2, "لوبیا سبز", "green-beans", "🫛", 0, 9),
    (46, 2, "کلم", "cabbage", "🥬", 0, 10),
    (64, 2, "قارچ", "mushroom", "🍄", 0, 11),
    (63, 2, "کدو سبز", "zucchini", "🥒", 0, 12),
    (66, 2, "کاهو", "lettuce", "🥬", 0, 13),
    (67, 2, "اسفناج", "spinach", "🥬", 0, 14),
    (62, 2, "فلفل تند", "chili", "🌶", 0, 15),
    (72, 2, "پیازچه", "spring-onion", "🧅", 0, 16),
    (68, 2, "کرفس", "celery", "🥬", 0, 17),
    (69, 2, "گل‌کلم", "cauliflower", "🥦", 0, 18),
    (70, 2, "کلم بروکلی", "broccoli", "🥦", 0, 19),
    (74, 2, "نخودفرنگی", "green-peas", "🟢", 0, 20),
    (75, 2, "ذرت", "corn", "🌽", 0, 21),
    (71, 2, "بامیه", "okra", "🟢", 0, 22),
    (73, 2, "کدو حلوایی", "pumpkin", "🎃", 0, 23),
    (78, 2, "تره‌فرنگی", "leek", "🥬", 0, 24),
    (76, 2, "شلغم", "turnip", "🟣", 0, 25),
    (77, 2, "چغندر", "beet", "🟣", 0, 26),
    (166, 2, "برگ مو", "grape-leaf", "🍃", 0, 27),
    # ── غلات و نان ────────────────────────────────────────
    (14, 3, "برنج", "rice", "🍚", 0, 1),
    (15, 3, "نان", "bread", "🥖", 1, 2),
    (88, 3, "ماکارونی", "pasta", "🍝", 0, 3),
    (43, 3, "رشته آش", "ash-noodles", "🍜", 0, 4),
    (89, 3, "رشته پلویی", "reshteh-polo", "🍜", 0, 5),
    (159, 3, "آرد سفید", "flour", "🌾", 1, 6),
    (90, 3, "بلغور", "bulgur", "🌾", 0, 7),
    (91, 3, "جو", "barley", "🌾", 0, 8),
    (92, 3, "جو دوسر", "oats", "🌾", 0, 9),
    (160, 3, "نشاسته", "starch", "⚪", 0, 10),
    (161, 3, "بیکینگ پودر", "baking-powder", "⚪", 0, 11),
    (162, 3, "خمیرمایه", "yeast", "⚪", 0, 12),
    (163, 3, "آرد نخودچی", "chickpea-flour", "🌾", 0, 13),
    (164, 3, "گندم", "wheat", "🌾", 0, 14),
    # ── حبوبات ────────────────────────────────────────────
    (16, 4, "عدس", "lentil", "🫘", 0, 1),
    (41, 4, "نخود", "chickpea", "🫘", 0, 2),
    (17, 4, "لوبیا قرمز", "red-beans", "🫘", 0, 3),
    (42, 4, "لوبیا سفید", "white-beans", "🫘", 0, 4),
    (95, 4, "لوبیا چیتی", "pinto-beans", "🫘", 0, 5),
    (33, 4, "لپه", "split-peas", "🫘", 0, 6),
    (39, 4, "باقالی", "fava", "🫘", 0, 7),
    (96, 4, "لوبیا چشم‌بلبلی", "black-eyed-pea", "🫘", 0, 8),
    (97, 4, "ماش", "mung", "🫘", 0, 9),
    # ── لبنیات ────────────────────────────────────────────
    (31, 5, "تخم‌مرغ", "egg", "🥚", 0, 1),
    (18, 5, "ماست", "yogurt", "🥛", 0, 2),
    (98, 5, "شیر", "milk", "🥛", 0, 3),
    (99, 5, "پنیر", "cheese", "🧀", 0, 4),
    (37, 5, "کره", "butter", "🧈", 1, 5),
    (52, 5, "ماست چکیده", "strained-yogurt", "🥛", 0, 6),
    (19, 5, "کشک", "kashk", "🥛", 0, 7),
    (100, 5, "خامه", "cream", "🥛", 0, 8),
    (101, 5, "پنیر پیتزا", "pizza-cheese", "🧀", 0, 9),
    (167, 5, "دوغ", "doogh", "🥛", 0, 10),
    # ── سبزی تازه ─────────────────────────────────────────
    (79, 6, "جعفری", "parsley", "🌿", 0, 1),
    (80, 6, "گشنیز", "cilantro", "🌿", 0, 2),
    (40, 6, "شوید", "dill", "🌿", 0, 3),
    (81, 6, "نعناع تازه", "fresh-mint", "🌿", 0, 4),
    (82, 6, "ریحان", "basil", "🌿", 0, 5),
    (11, 6, "سبزی قورمه", "herb-ghorme", "🌿", 0, 6),
    (47, 6, "سبزی پلویی", "herb-polo", "🌿", 0, 7),
    (48, 6, "سبزی کوکو", "herb-kuku", "🌿", 0, 8),
    (49, 6, "سبزی آش", "herb-ash", "🌿", 0, 9),
    (53, 6, "سبزی معطر", "aromatic-herbs", "🌿", 0, 10),
    (85, 6, "تره", "tareh", "🌿", 0, 11),
    (83, 6, "ترخون", "tarragon", "🌿", 0, 12),
    (84, 6, "مرزه", "savory", "🌿", 0, 13),
    (86, 6, "شاهی", "cress", "🌿", 0, 14),
    # ── ادویه‌ها ───────────────────────────────────────────
    (22, 7, "نمک", "salt", "🧂", 1, 1),
    (23, 7, "فلفل سیاه", "pepper", "🌶", 1, 2),
    (20, 7, "زردچوبه", "turmeric", "🟡", 1, 3),
    (103, 7, "فلفل قرمز", "red-pepper", "🔴", 1, 4),
    (24, 7, "دارچین", "cinnamon", "🟤", 1, 5),
    (104, 7, "زیره", "cumin", "🟤", 1, 6),
    (105, 7, "سماق", "sumac", "🔴", 1, 7),
    (44, 7, "نعناع خشک", "dried-mint", "🌿", 1, 8),
    (21, 7, "زعفران", "saffron", "🟡", 0, 9),
    (106, 7, "گلپر", "golpar", "🌿", 1, 10),
    (111, 7, "ادویه پلویی", "advieh-polo", "🧂", 1, 11),
    (107, 7, "هل", "cardamom", "🟢", 0, 12),
    (108, 7, "زنجبیل", "ginger", "🟠", 0, 13),
    (109, 7, "پودر سیر", "garlic-powder", "⚪", 1, 14),
    (110, 7, "آویشن", "thyme", "🌿", 0, 15),
    (114, 7, "پاپریکا", "paprika", "🔴", 0, 16),
    (112, 7, "پودر کاری", "curry-powder", "🟡", 0, 17),
    (116, 7, "میخک", "clove", "🟤", 0, 18),
    (119, 7, "سیاه‌دانه", "nigella", "⚫", 0, 19),
    (120, 7, "تخم گشنیز", "coriander-seed", "🟢", 0, 20),
    # ── چاشنی و روغن ──────────────────────────────────────
    (26, 8, "روغن مایع", "oil", "🫒", 1, 1),
    (25, 8, "رب گوجه", "tomato-paste", "🍅", 1, 2),
    (28, 8, "آبلیمو", "lime-juice", "🍋", 1, 3),
    (27, 8, "سرکه", "vinegar", "🍶", 1, 4),
    (121, 8, "روغن زیتون", "olive-oil", "🫒", 0, 5),
    (32, 8, "لیموعمانی", "dried-lime", "🍋", 0, 6),
    (50, 8, "آبغوره", "verjuice", "🍇", 0, 7),
    (35, 8, "رب انار", "pomegranate-paste", "🔴", 0, 8),
    (128, 8, "آب نارنج", "sour-orange", "🍊", 0, 9),
    (123, 8, "روغن حیوانی", "ghee", "🧈", 0, 10),
    (122, 8, "روغن کنجد", "sesame-oil", "🫒", 0, 11),
    (124, 8, "مایونز", "mayo", "🫙", 0, 12),
    (125, 8, "کچاپ", "ketchup", "🍅", 0, 13),
    (127, 8, "سس سویا", "soy-sauce", "🫙", 0, 14),
    (126, 8, "خردل", "mustard", "🟡", 0, 15),
    (130, 8, "رب فلفل", "pepper-paste", "🔴", 0, 16),
    # ── کنسرو و ترشی ──────────────────────────────────────
    (54, 9, "خیارشور", "pickle", "🥒", 0, 1),
    (55, 9, "زیتون", "olive", "🫒", 0, 2),
    (131, 9, "ترشی مخلوط", "mixed-pickle", "🫙", 0, 3),
    (132, 9, "سیرترشی", "pickled-garlic", "🧄", 0, 4),
    (137, 9, "زیتون پرورده", "marinated-olive", "🫒", 0, 5),
    (135, 9, "غوره", "sour-grape", "🍇", 0, 6),
    (133, 9, "کنسرو ذرت", "canned-corn", "🌽", 0, 7),
    (134, 9, "کنسرو لوبیا", "canned-beans", "🥫", 0, 8),
    # ── خشکبار و میوه ─────────────────────────────────────
    (36, 10, "شکر", "sugar", "🍬", 1, 1),
    (144, 10, "عسل", "honey", "🍯", 0, 2),
    (148, 10, "لیموترش", "lemon", "🍋", 0, 3),
    (150, 10, "سیب", "apple", "🍎", 0, 4),
    (151, 10, "انار", "pomegranate", "🍎", 0, 5),
    (29, 10, "زرشک", "barberry", "🔴", 0, 6),
    (38, 10, "کشمش", "raisin", "🍇", 0, 7),
    (34, 10, "گردو", "walnut", "🥜", 0, 8),
    (138, 10, "بادام", "almond", "🥜", 0, 9),
    (139, 10, "پسته", "pistachio", "🟢", 0, 10),
    (141, 10, "خرما", "date", "🟤", 0, 11),
    (30, 10, "آلو بخارا", "plum", "🟣", 0, 12),
    (140, 10, "فندق", "hazelnut", "🟤", 0, 13),
    (147, 10, "کنجد", "sesame", "⚪", 0, 14),
    (143, 10, "برگه زردآلو", "dried-apricot", "🟠", 0, 15),
    (142, 10, "توت خشک", "dried-mulberry", "🟣", 0, 16),
    (152, 10, "به", "quince", "🟡", 0, 17),
    (149, 10, "پرتقال", "orange", "🍊", 0, 18),
    (153, 10, "موز", "banana", "🍌", 0, 19),
    (145, 10, "پودر کاکائو", "cocoa", "🍫", 0, 20),
    (146, 10, "وانیل", "vanilla", "⚪", 0, 21),
    (165, 10, "آلبالو", "sour-cherry", "🍒", 0, 22),
]

RECIPE_CATEGORIES = [
    (1, "خورش و خوراک", "stew", "🥘", 1),
    (2, "پلو و چلو", "polo", "🍚", 2),
    (3, "غذای سنتی", "traditional", "🍲", 3),
    (4, "کباب", "kebab", "🍖", 4),
    (5, "آش و سوپ", "ash", "🥣", 5),
    (6, "کوکو و کتلت", "kuku", "🌿", 6),
    (7, "غذای روزمره", "everyday", "🍳", 7),
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

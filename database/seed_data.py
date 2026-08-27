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
    {
        "id": 1,
        "category_id": 1,
        "name": "قورمه‌سبزی",
        "slug": "ghorme-sabzi",
        "emoji": "🍲",
        "description": "خورش سنتی ایرانی با سبزی سرخ‌شده، لوبیا قرمز و لیموعمانی.",
        "instructions": (
            "1. پیاز را خرد کن و تفت بده.\n"
            "2. گوشت و زردچوبه را اضافه کن و همراه پیاز تفت بده.\n"
            "3. سبزی قورمه را جداگانه خوب سرخ کن.\n"
            "4. سبزی سرخ‌شده و لوبیای از قبل خیس‌خورده را به گوشت اضافه کن.\n"
            "5. آب بریز و حدود ۲ ساعت بپز.\n"
            "6. در نیمه دوم پخت، لیموعمانی سوراخ‌شده را اضافه کن و اجازه بده خورش جا بیفتد."
        ),
        "prep_time": 30,
        "cook_time": 120,
        "servings": 4,
        "difficulty": "hard",
        "cost_level": "medium",
        "is_vegetarian": 0,
        "ingredients": [
            _ing(2, "۴۰۰", "گرم", 10),
            _ing(11, "۵۰۰", "گرم", 10),
            _ing(17, "۱", "پیمانه", 8),
            _ing(7, "۱", "عدد", 6),
            _ing(32, "۴", "عدد", 8),
            _ing(26, "به اندازه نیاز", "", 1, **_OPT),
            _ing(20, "به اندازه نیاز", "", 1, **_OPT),
            _ing(22, "به اندازه نیاز", "", 1, **_OPT),
            _ing(23, "به اندازه نیاز", "", 1, **_OPT),
        ],
    },
    {
        "id": 2,
        "category_id": 1,
        "name": "قیمه سیب‌زمینی",
        "slug": "gheymeh",
        "emoji": "🍛",
        "description": "خورش گوشت و لپه با رب گوجه، لیموعمانی و خلال سیب‌زمینی سرخ‌شده.",
        "instructions": (
            "1. پیاز و گوشت را تفت بده.\n"
            "2. لپه و رب گوجه را اضافه کن و کمی سرخ کن.\n"
            "3. آب و لیموعمانی را اضافه کن و حدود ۹۰ دقیقه بپز.\n"
            "4. سیب‌زمینی‌ها را خلالی سرخ کن.\n"
            "5. هنگام سرو، خلال سیب‌زمینی را روی خورش بریز."
        ),
        "prep_time": 25,
        "cook_time": 90,
        "servings": 4,
        "difficulty": "medium",
        "cost_level": "medium",
        "is_vegetarian": 0,
        "ingredients": [
            _ing(2, "۳۵۰", "گرم", 10),
            _ing(33, "۱", "پیمانه", 10),
            _ing(7, "۱", "عدد", 6),
            _ing(25, "۲", "قاشق", 8),
            _ing(32, "۳", "عدد", 8),
            _ing(8, "۳", "عدد", 6),
            _ing(20, "به اندازه نیاز", "", 1, **_OPT),
            _ing(24, "به اندازه نیاز", "", 3, **_OPT),
            _ing(22, "به اندازه نیاز", "", 1, **_OPT),
            _ing(23, "به اندازه نیاز", "", 1, **_OPT),
            _ing(26, "به اندازه نیاز", "", 1, **_OPT),
        ],
    },
    {
        "id": 3,
        "category_id": 2,
        "name": "زرشک‌پلو با مرغ",
        "slug": "zereshk-polo",
        "emoji": "🍗",
        "description": "برنج زعفرانی با مرغ، زرشک تفت‌داده‌شده و کمی طعم شیرین و ترش.",
        "instructions": (
            "1. مرغ را با پیاز و ادویه تفت بده.\n"
            "2. رب گوجه و کمی آب اضافه کن و بپز تا مرغ بپزد.\n"
            "3. برنج را آبکش و دم کن.\n"
            "4. زرشک را با کره، مقدار کمی شکر و زعفران چند دقیقه تفت بده.\n"
            "5. زرشک را همراه برنج و مرغ سرو کن."
        ),
        "prep_time": 20,
        "cook_time": 55,
        "servings": 4,
        "difficulty": "medium",
        "cost_level": "medium",
        "is_vegetarian": 0,
        "ingredients": [
            _ing(1, "۴", "تکه", 10),
            _ing(14, "۳", "پیمانه", 10),
            _ing(29, "۱", "پیمانه", 8),
            _ing(7, "۱", "عدد", 6),
            _ing(25, "۱", "قاشق", 5),
            _ing(21, "به اندازه نیاز", "", 5),
            _ing(36, "مقدار کم", "", 3, **_OPT),
            _ing(37, "به اندازه نیاز", "", 3, **_OPT),
            _ing(22, "به اندازه نیاز", "", 1, **_OPT),
            _ing(23, "به اندازه نیاز", "", 1, **_OPT),
            _ing(26, "به اندازه نیاز", "", 1, **_OPT),
        ],
    },
    {
        "id": 4,
        "category_id": 1,
        "name": "فسنجان",
        "slug": "fesenjan",
        "emoji": "🥘",
        "description": "خورش مرغ با گردوی آسیاب‌شده و رب انار که آرام پخته و روغن می‌اندازد.",
        "instructions": (
            "1. گردو را چند دقیقه تفت بده.\n"
            "2. حدود ۳ پیمانه آب سرد اضافه کن.\n"
            "3. اجازه بده آرام بجوشد تا روغن بیندازد.\n"
            "4. پیاز و مرغ تفت‌داده‌شده را اضافه کن.\n"
            "5. رب انار را بریز.\n"
            "6. ۲ تا ۳ ساعت با حرارت کم بپز. در صورت تمایل کمی شکر اضافه کن."
        ),
        "prep_time": 20,
        "cook_time": 150,
        "servings": 4,
        "difficulty": "hard",
        "cost_level": "high",
        "is_vegetarian": 0,
        "ingredients": [
            _ing(1, "۴", "تکه", 10),
            _ing(34, "۳۰۰", "گرم", 10),
            _ing(35, "۴ تا ۵", "قاشق", 10),
            _ing(7, "۱", "عدد", 6),
            _ing(36, "در صورت تمایل", "", 2, **_OPT),
            _ing(22, "به اندازه نیاز", "", 1, **_OPT),
            _ing(23, "به اندازه نیاز", "", 1, **_OPT),
            _ing(26, "به اندازه نیاز", "", 1, **_OPT),
        ],
    },
    {
        "id": 5,
        "category_id": 2,
        "name": "ته‌چین مرغ",
        "slug": "tahchin-morgh",
        "emoji": "🍚",
        "description": "برنج مخلوط با ماست و زعفران که با مرغ ریش‌ریش لایه‌لایه دم می‌شود.",
        "instructions": (
            "1. مرغ را بپز و ریش‌ریش کن.\n"
            "2. برنج را نیم‌پز کن.\n"
            "3. ماست چکیده، تخم‌مرغ، زعفران و روغن را مخلوط کن و با برنج ترکیب کن.\n"
            "4. نصف برنج را در قابلمه بریز، مرغ را وسط قرار بده و بقیه برنج را اضافه کن.\n"
            "5. حدود ۵۰ تا ۶۰ دقیقه دم بده. در صورت تمایل با زرشک سرو کن."
        ),
        "prep_time": 30,
        "cook_time": 60,
        "servings": 4,
        "difficulty": "hard",
        "cost_level": "medium",
        "is_vegetarian": 0,
        "ingredients": [
            _ing(14, "۳", "پیمانه", 10),
            _ing(1, "۳۰۰", "گرم", 10),
            _ing(52, "۱", "پیمانه", 10),
            _ing(31, "۲", "عدد", 8),
            _ing(21, "به اندازه نیاز", "", 5),
            _ing(26, "به اندازه نیاز", "", 3),
            _ing(37, "به اندازه نیاز", "", 3, **_OPT),
            _ing(29, "برای سرو", "", 3, **_OPT),
            _ing(22, "به اندازه نیاز", "", 1, **_OPT),
        ],
    },
    {
        "id": 6,
        "category_id": 4,
        "name": "کباب کوبیده",
        "slug": "koobideh",
        "emoji": "🥩",
        "description": "گوشت چرخ‌کرده ورزداده‌شده با پیاز که روی سیخ کباب می‌شود.",
        "instructions": (
            "1. پیاز را رنده کن و آب آن را کاملاً بگیر.\n"
            "2. با گوشت، نمک و فلفل خوب ورز بده.\n"
            "3. چند ساعت در یخچال استراحت بده.\n"
            "4. گوشت را روی سیخ پهن کن و روی زغال یا کباب‌پز بپز.\n"
            "5. در پایان کمی کره و زعفران روی آن بزن."
        ),
        "prep_time": 30,
        "cook_time": 20,
        "servings": 4,
        "difficulty": "hard",
        "cost_level": "high",
        "is_vegetarian": 0,
        "ingredients": [
            _ing(3, "۶۰۰", "گرم", 10),
            _ing(7, "۲", "عدد", 8),
            _ing(22, "به اندازه نیاز", "", 5),
            _ing(23, "به اندازه نیاز", "", 5),
            _ing(21, "به اندازه نیاز", "", 3, **_OPT),
            _ing(37, "برای سرو", "", 2, **_OPT),
        ],
    },
    {
        "id": 7,
        "category_id": 4,
        "name": "جوجه‌کباب زعفرانی",
        "slug": "joojeh-kebab",
        "emoji": "🍗",
        "description": "مرغ بدون استخوان مزه‌دارشده با زعفران و پیاز که روی زغال کباب می‌شود.",
        "instructions": (
            "1. مرغ را تکه کن.\n"
            "2. با پیاز، زعفران، روغن و فلفل چند ساعت مزه‌دار کن.\n"
            "3. نمک و آبلیمو را نزدیک زمان پخت اضافه کن.\n"
            "4. به سیخ بکش و روی زغال کباب کن."
        ),
        "prep_time": 20,
        "cook_time": 25,
        "servings": 4,
        "difficulty": "medium",
        "cost_level": "medium",
        "is_vegetarian": 0,
        "ingredients": [
            _ing(1, "۷۰۰", "گرم", 10),
            _ing(7, "۲", "عدد", 8),
            _ing(21, "به اندازه نیاز", "", 8),
            _ing(28, "به اندازه نیاز", "", 5),
            _ing(26, "به اندازه نیاز", "", 3),
            _ing(22, "به اندازه نیاز", "", 3),
            _ing(23, "به اندازه نیاز", "", 3),
        ],
    },
    {
        "id": 8,
        "category_id": 2,
        "name": "عدس‌پلو",
        "slug": "adas-polo",
        "emoji": "🍚",
        "description": "برنج مخلوط با عدس، همراه گوشت تفت‌داده‌شده و کشمش.",
        "instructions": (
            "1. عدس را جدا بپز.\n"
            "2. برنج را نیم‌پز کن، با عدس مخلوط کن و دم بده.\n"
            "3. گوشت را با پیاز و ادویه تفت بده.\n"
            "4. کشمش را کمی تفت بده.\n"
            "5. هنگام سرو، گوشت و کشمش را روی عدس‌پلو بریز."
        ),
        "prep_time": 20,
        "cook_time": 50,
        "servings": 4,
        "difficulty": "medium",
        "cost_level": "low",
        "is_vegetarian": 0,
        "ingredients": [
            _ing(14, "۳", "پیمانه", 10),
            _ing(16, "۱.۵", "پیمانه", 10),
            _ing(3, "۲۵۰", "گرم", 8),
            _ing(7, "به اندازه نیاز", "", 6),
            _ing(38, "به اندازه نیاز", "", 5),
            _ing(24, "به اندازه نیاز", "", 3, **_OPT),
            _ing(21, "به اندازه نیاز", "", 3, **_OPT),
            _ing(22, "به اندازه نیاز", "", 1, **_OPT),
            _ing(26, "به اندازه نیاز", "", 1, **_OPT),
        ],
    },
    {
        "id": 9,
        "category_id": 2,
        "name": "لوبیاپلو",
        "slug": "loobia-polo",
        "emoji": "🍅",
        "description": "برنج لایه‌لایه با لوبیا سبز، گوشت و رب گوجه که دم کشیده می‌شود.",
        "instructions": (
            "1. پیاز و گوشت را تفت بده.\n"
            "2. لوبیای خردشده و رب را اضافه کن و اجازه بده مواد بپزند.\n"
            "3. برنج را آبکش کن.\n"
            "4. لایه‌لایه با مواد داخل قابلمه بریز.\n"
            "5. حدود ۴۵ دقیقه دم بده."
        ),
        "prep_time": 20,
        "cook_time": 45,
        "servings": 4,
        "difficulty": "medium",
        "cost_level": "medium",
        "is_vegetarian": 0,
        "ingredients": [
            _ing(14, "۳", "پیمانه", 10),
            _ing(12, "۴۰۰", "گرم", 10),
            _ing(3, "۳۰۰", "گرم", 10),
            _ing(25, "۲", "قاشق", 8),
            _ing(7, "به اندازه نیاز", "", 6),
            _ing(24, "به اندازه نیاز", "", 3, **_OPT),
            _ing(20, "به اندازه نیاز", "", 3, **_OPT),
            _ing(22, "به اندازه نیاز", "", 1, **_OPT),
            _ing(26, "به اندازه نیاز", "", 1, **_OPT),
        ],
    },
    {
        "id": 10,
        "category_id": 2,
        "name": "باقالی‌پلو با ماهیچه",
        "slug": "baghali-polo",
        "emoji": "🍖",
        "description": "برنج با باقالی و شوید، در کنار ماهیچه که آرام پخته شده است.",
        "instructions": (
            "1. ماهیچه را با پیاز و ادویه تفت بده.\n"
            "2. با آب کم چند ساعت بپز تا نرم شود.\n"
            "3. برنج، باقالی و شوید را آبکش و دم کن.\n"
            "4. با کره و زعفران سرو کن."
        ),
        "prep_time": 25,
        "cook_time": 180,
        "servings": 4,
        "difficulty": "hard",
        "cost_level": "high",
        "is_vegetarian": 0,
        "ingredients": [
            _ing(14, "۳", "پیمانه", 10),
            _ing(39, "۲", "پیمانه", 10),
            _ing(40, "به اندازه نیاز", "", 8),
            _ing(51, "۴", "عدد", 10),
            _ing(7, "به اندازه نیاز", "", 6),
            _ing(21, "به اندازه نیاز", "", 5),
            _ing(37, "برای سرو", "", 3, **_OPT),
            _ing(20, "به اندازه نیاز", "", 1, **_OPT),
            _ing(22, "به اندازه نیاز", "", 1, **_OPT),
            _ing(23, "به اندازه نیاز", "", 1, **_OPT),
        ],
    },
    {
        "id": 11,
        "category_id": 5,
        "name": "آش رشته",
        "slug": "ash-reshteh",
        "emoji": "🥣",
        "description": "آش حبوبات با سبزی، رشته، کشک و تزئین پیازداغ و نعناع‌داغ.",
        "instructions": (
            "1. نخود، لوبیا و عدس خیس‌خورده را بپز.\n"
            "2. سبزی آش را اضافه کن و اجازه بده نرم شود.\n"
            "3. رشته را بریز و مرتب هم بزن تا نچسبد.\n"
            "4. در پایان کشک اضافه کن.\n"
            "5. با پیازداغ، سیرداغ و نعناع‌داغ تزئین کن."
        ),
        "prep_time": 20,
        "cook_time": 90,
        "servings": 6,
        "difficulty": "medium",
        "cost_level": "low",
        "is_vegetarian": 1,
        "ingredients": [
            _ing(41, "۱", "پیمانه", 8),
            _ing(17, "۱", "پیمانه", 8),
            _ing(16, "۱", "پیمانه", 8),
            _ing(49, "۷۰۰", "گرم", 10),
            _ing(43, "۳۰۰", "گرم", 10),
            _ing(19, "به اندازه نیاز", "", 8),
            _ing(7, "به اندازه نیاز", "", 6),
            _ing(45, "به اندازه نیاز", "", 5),
            _ing(44, "به اندازه نیاز", "", 5),
            _ing(26, "به اندازه نیاز", "", 1, **_OPT),
            _ing(22, "به اندازه نیاز", "", 1, **_OPT),
        ],
    },
    {
        "id": 12,
        "category_id": 3,
        "name": "کشک بادمجان",
        "slug": "kashk-bademjan",
        "emoji": "🍆",
        "description": "بادمجان سرخ یا کبابی‌شده با پیازداغ، سیر، کشک، نعناع‌داغ و گردو.",
        "instructions": (
            "1. بادمجان‌ها را سرخ یا کبابی کن و له کن.\n"
            "2. با پیازداغ و سیر چند دقیقه تفت بده.\n"
            "3. کشک و کمی آب اضافه کن و اجازه بده مواد یکدست شوند.\n"
            "4. با نعناع‌داغ و گردو سرو کن."
        ),
        "prep_time": 15,
        "cook_time": 30,
        "servings": 4,
        "difficulty": "easy",
        "cost_level": "low",
        "is_vegetarian": 1,
        "ingredients": [
            _ing(10, "۵", "عدد", 10),
            _ing(19, "۱", "پیمانه", 10),
            _ing(7, "۲", "عدد", 6),
            _ing(45, "۳", "حبه", 6),
            _ing(34, "به اندازه نیاز", "", 3, **_OPT),
            _ing(44, "به اندازه نیاز", "", 5),
            _ing(26, "به اندازه نیاز", "", 1, **_OPT),
            _ing(22, "به اندازه نیاز", "", 1, **_OPT),
        ],
    },
    {
        "id": 13,
        "category_id": 3,
        "name": "میرزا قاسمی",
        "slug": "mirza-ghasemi",
        "emoji": "🍆",
        "description": "بادمجان کبابی با سیر، گوجه و تخم‌مرغ؛ غذای سنتی گیلان.",
        "instructions": (
            "1. بادمجان‌ها را کبابی کن، پوست بگیر و ساطوری کن.\n"
            "2. سیر را تفت بده.\n"
            "3. بادمجان و سپس گوجه خردشده را اضافه کن.\n"
            "4. وقتی آب مواد کم شد، تخم‌مرغ‌ها را اضافه و مخلوط کن."
        ),
        "prep_time": 15,
        "cook_time": 30,
        "servings": 4,
        "difficulty": "easy",
        "cost_level": "low",
        "is_vegetarian": 1,
        "ingredients": [
            _ing(10, "۵", "عدد", 10),
            _ing(9, "۴", "عدد", 8),
            _ing(31, "۳", "عدد", 8),
            _ing(45, "۵", "حبه", 8),
            _ing(26, "به اندازه نیاز", "", 1, **_OPT),
            _ing(22, "به اندازه نیاز", "", 1, **_OPT),
            _ing(23, "به اندازه نیاز", "", 1, **_OPT),
        ],
    },
    {
        "id": 14,
        "category_id": 3,
        "name": "آبگوشت",
        "slug": "abgoosht",
        "emoji": "🥘",
        "description": "گوشت با استخوان، نخود و لوبیا که پس از پخت به آبگوشت و گوشت‌کوبیده تقسیم می‌شود.",
        "instructions": (
            "1. گوشت، حبوبات خیس‌خورده، پیاز و زردچوبه را با آب بپز.\n"
            "2. بعد از نرم شدن گوشت، سیب‌زمینی، رب و لیموعمانی را اضافه کن.\n"
            "3. پس از پخت کامل، آب آن را جدا کن.\n"
            "4. گوشت و حبوبات را برای گوشت‌کوبیده بکوب."
        ),
        "prep_time": 20,
        "cook_time": 150,
        "servings": 4,
        "difficulty": "hard",
        "cost_level": "medium",
        "is_vegetarian": 0,
        "ingredients": [
            _ing(2, "۵۰۰", "گرم", 10),
            _ing(41, "۱", "پیمانه", 8),
            _ing(42, "۱", "پیمانه", 8),
            _ing(8, "۳", "عدد", 6),
            _ing(25, "به اندازه نیاز", "", 5),
            _ing(9, "به اندازه نیاز", "", 3, **_OPT),
            _ing(7, "به اندازه نیاز", "", 6),
            _ing(32, "به اندازه نیاز", "", 5),
            _ing(20, "به اندازه نیاز", "", 3),
            _ing(22, "به اندازه نیاز", "", 1, **_OPT),
        ],
    },
    {
        "id": 15,
        "category_id": 2,
        "name": "کلم‌پلو شیرازی",
        "slug": "kalam-polo",
        "emoji": "🍚",
        "description": "برنج دم‌شده با کلم و سبزی معطر، همراه کوفته‌ریزه گوشت.",
        "instructions": (
            "1. کلم خردشده را با پیاز و ادویه تفت بده.\n"
            "2. گوشت را به شکل کوفته‌ریزه آماده و سرخ کن.\n"
            "3. برنج نیم‌پز را با کلم و سبزی لایه‌لایه دم بده.\n"
            "4. با کوفته‌ریزه سرو کن."
        ),
        "prep_time": 30,
        "cook_time": 50,
        "servings": 4,
        "difficulty": "hard",
        "cost_level": "medium",
        "is_vegetarian": 0,
        "ingredients": [
            _ing(14, "۳", "پیمانه", 10),
            _ing(46, "۵۰۰", "گرم", 10),
            _ing(3, "۳۰۰", "گرم", 10),
            _ing(53, "به اندازه نیاز", "", 6),
            _ing(7, "به اندازه نیاز", "", 6),
            _ing(20, "به اندازه نیاز", "", 3, **_OPT),
            _ing(22, "به اندازه نیاز", "", 1, **_OPT),
            _ing(23, "به اندازه نیاز", "", 1, **_OPT),
            _ing(26, "به اندازه نیاز", "", 1, **_OPT),
        ],
    },
    {
        "id": 16,
        "category_id": 2,
        "name": "سبزی‌پلو با ماهی",
        "slug": "sabzi-polo-mahi",
        "emoji": "🐟",
        "description": "برنج مخلوط با سبزی پلویی در کنار ماهی مزه‌دار سرخ یا گریل‌شده.",
        "instructions": (
            "1. ماهی را با نمک، فلفل، آبلیمو و زعفران مزه‌دار کن.\n"
            "2. ماهی را سرخ یا گریل کن.\n"
            "3. برنج نیم‌پز را با سبزی پلویی مخلوط و دم کن.\n"
            "4. سبزی‌پلو را کنار ماهی سرو کن."
        ),
        "prep_time": 20,
        "cook_time": 45,
        "servings": 4,
        "difficulty": "medium",
        "cost_level": "medium",
        "is_vegetarian": 0,
        "ingredients": [
            _ing(14, "۳", "پیمانه", 10),
            _ing(47, "۴۰۰", "گرم", 10),
            _ing(4, "۴", "تکه", 10),
            _ing(45, "به اندازه نیاز", "", 5),
            _ing(28, "به اندازه نیاز", "", 5),
            _ing(21, "به اندازه نیاز", "", 5),
            _ing(22, "به اندازه نیاز", "", 1, **_OPT),
            _ing(23, "به اندازه نیاز", "", 1, **_OPT),
            _ing(26, "به اندازه نیاز", "", 1, **_OPT),
        ],
    },
    {
        "id": 17,
        "category_id": 2,
        "name": "استانبولی پلو",
        "slug": "estamboli-polo",
        "emoji": "🍅",
        "description": "کته برنج با سیب‌زمینی و گوجه؛ گوشت چرخ‌کرده در صورت تمایل اضافه می‌شود.",
        "instructions": (
            "1. پیاز و سیب‌زمینی را تفت بده.\n"
            "2. گوجه یا رب و در صورت تمایل گوشت را اضافه کن.\n"
            "3. برنج شسته‌شده را همراه آب مناسب داخل مواد بریز.\n"
            "4. مانند کته بپز تا آب جذب شود و سپس دم بکشد."
        ),
        "prep_time": 15,
        "cook_time": 40,
        "servings": 4,
        "difficulty": "easy",
        "cost_level": "low",
        "is_vegetarian": 1,
        "ingredients": [
            _ing(14, "۳", "پیمانه", 10),
            _ing(8, "۲", "عدد", 8),
            _ing(9, "۴", "عدد", 6),
            _ing(25, "به اندازه نیاز", "", 4, **_OPT),
            _ing(7, "۱", "عدد", 6),
            _ing(3, "در صورت تمایل", "", 4, **_OPT),
            _ing(20, "به اندازه نیاز", "", 3, **_OPT),
            _ing(22, "به اندازه نیاز", "", 1, **_OPT),
            _ing(26, "به اندازه نیاز", "", 1, **_OPT),
        ],
    },
    {
        "id": 18,
        "category_id": 6,
        "name": "کتلت گوشت",
        "slug": "kotlet",
        "emoji": "🥔",
        "description": "مخلوط گوشت چرخ‌کرده، سیب‌زمینی و پیاز رنده‌شده که در تابه سرخ می‌شود.",
        "instructions": (
            "1. سیب‌زمینی و پیاز را رنده کن و آب اضافی را بگیر.\n"
            "2. با گوشت، تخم‌مرغ و ادویه مخلوط کن.\n"
            "3. کتلت‌ها را شکل بده.\n"
            "4. در روغن با حرارت متوسط دو طرفشان را سرخ کن."
        ),
        "prep_time": 20,
        "cook_time": 20,
        "servings": 4,
        "difficulty": "easy",
        "cost_level": "low",
        "is_vegetarian": 0,
        "ingredients": [
            _ing(3, "۳۰۰", "گرم", 10),
            _ing(8, "۴", "عدد", 10),
            _ing(31, "۲", "عدد", 8),
            _ing(7, "۱", "عدد", 6),
            _ing(20, "به اندازه نیاز", "", 3, **_OPT),
            _ing(22, "به اندازه نیاز", "", 1, **_OPT),
            _ing(23, "به اندازه نیاز", "", 1, **_OPT),
            _ing(26, "به اندازه نیاز", "", 1, **_OPT),
        ],
    },
    {
        "id": 19,
        "category_id": 6,
        "name": "کوکو سبزی",
        "slug": "kuku-sabzi",
        "emoji": "🌿",
        "description": "کوکوی سبزی با تخم‌مرغ؛ گردو و زرشک در صورت تمایل اضافه می‌شود.",
        "instructions": (
            "1. سبزی خردشده را با تخم‌مرغ و ادویه مخلوط کن.\n"
            "2. در صورت تمایل گردو و زرشک اضافه کن.\n"
            "3. مواد را داخل تابه بریز.\n"
            "4. با حرارت ملایم هر دو طرف را بپز."
        ),
        "prep_time": 15,
        "cook_time": 25,
        "servings": 4,
        "difficulty": "easy",
        "cost_level": "low",
        "is_vegetarian": 1,
        "ingredients": [
            _ing(48, "۵۰۰", "گرم", 10),
            _ing(31, "۴ تا ۵", "عدد", 10),
            _ing(34, "در صورت تمایل", "", 3, **_OPT),
            _ing(29, "در صورت تمایل", "", 3, **_OPT),
            _ing(22, "به اندازه نیاز", "", 1, **_OPT),
            _ing(23, "به اندازه نیاز", "", 1, **_OPT),
            _ing(20, "به اندازه نیاز", "", 1, **_OPT),
            _ing(26, "به اندازه نیاز", "", 1, **_OPT),
        ],
    },
    {
        "id": 20,
        "category_id": 1,
        "name": "خورش بادمجان",
        "slug": "khoresh-bademjan",
        "emoji": "🍆",
        "description": "خورش گوشت با بادمجان سرخ‌شده، گوجه، رب و کمی آبغوره.",
        "instructions": (
            "1. بادمجان‌ها را سرخ کن.\n"
            "2. پیاز و گوشت را با زردچوبه تفت بده و رب را اضافه کن.\n"
            "3. آب بریز و اجازه بده گوشت بپزد.\n"
            "4. در ۳۰ دقیقه پایانی بادمجان و گوجه را اضافه کن.\n"
            "5. در پایان کمی آبغوره بریز."
        ),
        "prep_time": 25,
        "cook_time": 90,
        "servings": 4,
        "difficulty": "medium",
        "cost_level": "medium",
        "is_vegetarian": 0,
        "ingredients": [
            _ing(2, "۴۰۰", "گرم", 10),
            _ing(10, "۵", "عدد", 10),
            _ing(9, "۳", "عدد", 6),
            _ing(7, "۱", "عدد", 6),
            _ing(25, "۲", "قاشق", 8),
            _ing(50, "به اندازه نیاز", "", 5),
            _ing(32, "به جای آبغوره", "", 3, **_OPT),
            _ing(22, "به اندازه نیاز", "", 1, **_OPT),
            _ing(20, "به اندازه نیاز", "", 3, **_OPT),
            _ing(23, "به اندازه نیاز", "", 1, **_OPT),
            _ing(26, "به اندازه نیاز", "", 1, **_OPT),
        ],
    },
]


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

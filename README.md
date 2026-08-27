# 🍲 غذا چی بپزم؟

ربات تلگرام فارسی برای پیشنهاد غذا بر اساس مواد موجود در آشپزخانه — با UI منومحور و تجربه شبیه Mini App داخل تلگرام.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8+-orange.svg)](https://www.mysql.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## ✨ قابلیت‌ها

- 🧺 **با مواد خونه چی بپزم؟** — انتخاب مواد با Checkbox و پیشنهاد هوشمند
- 🎲 **پیشنهاد شانسی** — با فیلتر (سریع، اقتصادی، گیاهی و …)
- 🔍 **جستجوی غذا** — بر اساس نام غذا یا مواد
- ❤️ **علاقه‌مندی‌ها** و 🕘 **تاریخچه**
- ⚙️ **تنظیمات** — مواد همیشگی، تعداد نفرات، رژیم غذایی
- 👑 **پنل ادمین** — آمار، مدیریت محتوا
- ⬅️ **ناوبری Back/Home** — stack-based، حفظ صفحه Pagination

---

## 🛠 تکنولوژی

| لایه | ابزار |
|------|--------|
| Bot | [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) |
| Database | MySQL 8+ با Connection Pool |
| Config | python-dotenv |
| Architecture | Handler → Service → Repository |

---

## 📁 ساختار پروژه

```
che_bepazam/
├── main.py                 # نقطه ورود
├── config.py
├── setup_db.py             # راه‌اندازی schema + seed
├── bot/
│   ├── handlers/           # start, pantry, recipe, search, admin, …
│   ├── keyboards/          # InlineKeyboard layouts
│   └── callbacks/router.py
├── services/               # منطق کسب‌وکار
├── database/
│   ├── schema.sql
│   ├── seed.sql            # ۳ غذای نمونه + مواد اولیه
│   └── repositories/
├── states/
├── utils/
└── tests/
```

---

## 🚀 راه‌اندازی

### پیش‌نیاز

- Python 3.11+
- MySQL 8+

### ۱. Clone

```bash
git clone https://github.com/qashqaeii/chibepazam.git
cd chibepazam
```

### ۲. محیط مجازی

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### ۳. وابستگی‌ها

```bash
pip install -r requirements.txt
```

### ۴. تنظیمات

```bash
copy .env.example .env   # Windows
# cp .env.example .env   # Linux / macOS
```

فایل `.env` را ویرایش کنید:

```env
BOT_TOKEN=your_bot_token_from_botfather
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=che_bepazam
ADMIN_IDS=your_telegram_user_id
```

> ⚠️ فایل `.env` را **هرگز** commit نکنید.

### ۵. دیتابیس

```bash
python setup_db.py
```

### ۶. اجرا

```bash
python main.py
```

---

## 🧪 تست Foundation

```bash
python tests/verify_foundation.py
```

---

## 🗄 Schema

جداول اصلی: `users`, `ingredients`, `ingredient_categories`, `recipes`, `recipe_ingredients`, `user_pantry`, `user_permanent_ingredients`, `user_favorites`, `user_history`, `user_settings`, `bot_events`, `admins`

جزئیات کامل در [`database/schema.sql`](database/schema.sql).

---

## 📋 Roadmap

- [ ] Ingredient Master Database (۱۵۰–۲۵۰ ماده + Alias)
- [ ] ۱۰۰ غذای ایرانی متصل به مواد استاندارد
- [ ] مواد غیرمجاز کاربر
- [ ] ارسال همگانی ادمین

---

## 📄 License

MIT — see [LICENSE](LICENSE).

---

## 👤 Author

[qashqaeii](https://github.com/qashqaeii)

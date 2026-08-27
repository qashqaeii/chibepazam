import re

from database.repositories.promotions import PromotionsRepository

DEFAULT_SLOT = "main_menu"
TELEGRAM_URL = re.compile(r"^https?://(t\.me|telegram\.me)/[\w_]+", re.I)


class PromotionService:
    def __init__(self):
        self.repo = PromotionsRepository()
        self._cache: dict[str, dict | None] = {}

    def _invalidate(self, slot: str = DEFAULT_SLOT) -> None:
        self._cache.pop(slot, None)

    @staticmethod
    def normalize_url(raw: str) -> str:
        text = (raw or "").strip()
        if not text:
            return ""
        if text.startswith("@"):
            return f"https://t.me/{text.lstrip('@')}"
        if text.startswith("t.me/"):
            return f"https://{text}"
        if not text.startswith("http"):
            return f"https://t.me/{text.lstrip('@')}"
        return text

    @staticmethod
    def is_valid_url(url: str) -> bool:
        return bool(url and TELEGRAM_URL.match(url))

    def get_active(self, slot: str = DEFAULT_SLOT) -> dict | None:
        try:
            if slot in self._cache:
                row = self._cache[slot]
            else:
                row = self.repo.get_by_slot(slot)
                self._cache[slot] = row
        except Exception:
            return None
        if not row or not row.get("is_active"):
            return None
        return row

    def get_config(self, slot: str = DEFAULT_SLOT) -> dict | None:
        try:
            return self.repo.get_by_slot(slot)
        except Exception:
            return None

    def toggle(self, slot: str = DEFAULT_SLOT) -> bool:
        row = self.repo.get_by_slot(slot)
        if not row:
            return False
        new_val = not bool(row.get("is_active"))
        self.repo.set_active(slot, new_val)
        self._invalidate(slot)
        return new_val

    def update_body(self, text: str, slot: str = DEFAULT_SLOT) -> None:
        self.repo.update_field(slot, "body_text", text.strip())
        self._invalidate(slot)

    def update_button(self, label: str, slot: str = DEFAULT_SLOT) -> None:
        self.repo.update_field(slot, "button_label", label.strip())
        self._invalidate(slot)

    def update_url(self, raw_url: str, slot: str = DEFAULT_SLOT) -> str:
        url = self.normalize_url(raw_url)
        if not self.is_valid_url(url):
            raise ValueError("invalid url")
        self.repo.update_field(slot, "link_url", url)
        self._invalidate(slot)
        return url

    def format_ad_block(self, slot: str = DEFAULT_SLOT) -> str | None:
        promo = self.get_active(slot)
        if not promo:
            return None
        from utils.menu_style import section

        body = promo.get("body_text") or ""
        title = promo.get("title") or "پیشنهاد ویژه"
        return section(f"📢 {title}", [body])

    def button_for_keyboard(self, slot: str = DEFAULT_SLOT) -> tuple[str, str] | None:
        promo = self.get_active(slot)
        if not promo:
            return None
        label = (promo.get("button_label") or "").strip()
        url = (promo.get("link_url") or "").strip()
        if label and url and self.is_valid_url(url):
            return label, url
        return None

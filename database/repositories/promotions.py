from database.connection import get_connection

SLOTS = ("main_menu",)


class PromotionsRepository:
    def get_by_slot(self, slot: str) -> dict | None:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM bot_promotions WHERE slot = %s LIMIT 1",
                (slot,),
            )
            return cursor.fetchone()
        finally:
            conn.close()

    def get_all(self) -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM bot_promotions ORDER BY sort_order, id")
            return cursor.fetchall()
        finally:
            conn.close()

    def upsert(
        self,
        slot: str,
        body_text: str,
        button_label: str,
        link_url: str,
        is_active: bool = True,
        title: str | None = None,
    ) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO bot_promotions (slot, title, body_text, button_label, link_url, is_active)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    title = VALUES(title),
                    body_text = VALUES(body_text),
                    button_label = VALUES(button_label),
                    link_url = VALUES(link_url),
                    is_active = VALUES(is_active),
                    updated_at = NOW()
                """,
                (slot, title, body_text, button_label, link_url, 1 if is_active else 0),
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def set_active(self, slot: str, active: bool) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE bot_promotions SET is_active = %s, updated_at = NOW() WHERE slot = %s",
                (1 if active else 0, slot),
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def update_field(self, slot: str, field: str, value: str) -> None:
        allowed = {"body_text", "button_label", "link_url", "title"}
        if field not in allowed:
            raise ValueError("invalid field")
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE bot_promotions SET {field} = %s, updated_at = NOW() WHERE slot = %s",
                (value, slot),
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

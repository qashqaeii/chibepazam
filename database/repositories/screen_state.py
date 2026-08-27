import json
from database.connection import get_connection


class ScreenStateRepository:
    def save(self, user_id: int, screen: str, payload: dict | None = None) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO user_screen_state (user_id, screen, payload)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE screen = VALUES(screen), payload = VALUES(payload), updated_at = NOW()
                """,
                (user_id, screen, json.dumps(payload or {}, ensure_ascii=False)),
            )
            conn.commit()
        except Exception:
            conn.rollback()
        finally:
            conn.close()

    def load(self, user_id: int) -> dict | None:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT screen, payload FROM user_screen_state WHERE user_id = %s",
                (user_id,),
            )
            row = cursor.fetchone()
            if not row:
                return None
            payload = row.get("payload")
            if isinstance(payload, str):
                payload = json.loads(payload)
            return {"screen": row["screen"], "payload": payload or {}}
        finally:
            conn.close()

    def clear(self, user_id: int) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user_screen_state WHERE user_id = %s", (user_id,))
            conn.commit()
        except Exception:
            conn.rollback()
        finally:
            conn.close()

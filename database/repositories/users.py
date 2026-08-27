from database.connection import get_connection
from utils.logger import setup_logger

logger = setup_logger(__name__)


class UsersRepository:
    def get_or_create(
        self,
        telegram_id: int,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> dict:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM users WHERE telegram_id = %s",
                (telegram_id,),
            )
            user = cursor.fetchone()
            if user:
                cursor.execute(
                    """UPDATE users SET username=%s, first_name=%s, last_name=%s,
                       last_seen_at=NOW(), is_active=1 WHERE telegram_id=%s""",
                    (username, first_name, last_name, telegram_id),
                )
                conn.commit()
                cursor.execute(
                    "SELECT * FROM users WHERE telegram_id = %s",
                    (telegram_id,),
                )
                return cursor.fetchone()

            cursor.execute(
                """INSERT INTO users (telegram_id, username, first_name, last_name)
                   VALUES (%s, %s, %s, %s)""",
                (telegram_id, username, first_name, last_name),
            )
            user_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO user_settings (user_id) VALUES (%s)",
                (user_id,),
            )
            conn.commit()
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            return cursor.fetchone()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_by_telegram_id(self, telegram_id: int) -> dict | None:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM users WHERE telegram_id = %s",
                (telegram_id,),
            )
            return cursor.fetchone()
        finally:
            conn.close()

    def get_by_id(self, user_id: int) -> dict | None:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            return cursor.fetchone()
        finally:
            conn.close()

    def count_all(self) -> int:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            return cursor.fetchone()[0]
        finally:
            conn.close()

    def count_active_today(self) -> int:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM users WHERE DATE(last_seen_at) = CURDATE()"
            )
            return cursor.fetchone()[0]
        finally:
            conn.close()

    def is_admin(self, telegram_id: int) -> bool:
        from config import Config
        if telegram_id in Config.ADMIN_IDS:
            return True
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM admins WHERE telegram_id = %s LIMIT 1",
                (telegram_id,),
            )
            return cursor.fetchone() is not None
        finally:
            conn.close()

    def push_nav(self, user_id: int, screen: str, payload: dict | None = None) -> None:
        import json
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user_nav_stack (user_id, screen, payload) VALUES (%s, %s, %s)",
                (user_id, screen, json.dumps(payload or {}, ensure_ascii=False)),
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def pop_nav(self, user_id: int) -> dict | None:
        import json
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """SELECT id, screen, payload FROM user_nav_stack
                   WHERE user_id = %s ORDER BY id DESC LIMIT 1""",
                (user_id,),
            )
            row = cursor.fetchone()
            if not row:
                return None
            cursor.execute("DELETE FROM user_nav_stack WHERE id = %s", (row["id"],))
            conn.commit()
            payload = row.get("payload")
            if isinstance(payload, str):
                payload = json.loads(payload)
            return {"screen": row["screen"], "payload": payload or {}}
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def clear_nav(self, user_id: int) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user_nav_stack WHERE user_id = %s", (user_id,))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_active_telegram_ids(self) -> list[int]:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT telegram_id FROM users WHERE is_active = 1 AND is_blocked = 0"
            )
            return [int(row[0]) for row in cursor.fetchall()]
        finally:
            conn.close()

    def count_favorites_total(self) -> int:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM user_favorites")
            return int(cursor.fetchone()[0])
        finally:
            conn.close()

    def top_pantry_ingredients(self, limit: int = 5) -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT i.name, i.emoji, COUNT(*) AS cnt
                FROM user_pantry up
                JOIN ingredients i ON i.id = up.ingredient_id
                GROUP BY i.id ORDER BY cnt DESC LIMIT %s
                """,
                (limit,),
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def get_active_telegram_ids(self) -> list[int]:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT telegram_id FROM users WHERE is_active = 1 AND is_blocked = 0"
            )
            return [int(row[0]) for row in cursor.fetchall()]
        finally:
            conn.close()

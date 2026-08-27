from database.connection import get_connection
from config import Config


class HistoryRepository:
    def add(self, user_id: int, recipe_id: int) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user_history (user_id, recipe_id) VALUES (%s, %s)",
                (user_id, recipe_id),
            )
            cursor.execute(
                """DELETE FROM user_history WHERE user_id = %s AND id NOT IN (
                   SELECT id FROM (
                       SELECT id FROM user_history
                       WHERE user_id = %s ORDER BY viewed_at DESC
                       LIMIT %s
                   ) t
                )""",
                (user_id, user_id, Config.HISTORY_MAX),
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_recent(self, user_id: int, limit: int = 10) -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """SELECT r.*, uh.viewed_at
                   FROM user_history uh
                   JOIN recipes r ON r.id = uh.recipe_id
                   WHERE uh.user_id = %s
                   ORDER BY uh.viewed_at DESC
                   LIMIT %s""",
                (user_id, limit),
            )
            return cursor.fetchall()
        finally:
            conn.close()

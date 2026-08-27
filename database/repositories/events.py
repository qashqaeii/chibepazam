import json
from database.connection import get_connection


class EventsRepository:
    def log(self, event_type: str, user_id: int | None = None, data: dict | None = None) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO bot_events (user_id, event_type, event_data) VALUES (%s, %s, %s)",
                (user_id, event_type, json.dumps(data or {}, ensure_ascii=False)),
            )
            conn.commit()
        except Exception:
            conn.rollback()
        finally:
            conn.close()

    def count_today(self, event_type: str) -> int:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT COUNT(*) FROM bot_events
                   WHERE event_type = %s AND DATE(created_at) = CURDATE()""",
                (event_type,),
            )
            return cursor.fetchone()[0]
        finally:
            conn.close()

    def log_search(self, user_id: int, query: str) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user_search_history (user_id, query) VALUES (%s, %s)",
                (user_id, query),
            )
            conn.commit()
        except Exception:
            conn.rollback()
        finally:
            conn.close()

    def count_searches_today(self) -> int:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM user_search_history WHERE DATE(searched_at) = CURDATE()"
            )
            return cursor.fetchone()[0]
        finally:
            conn.close()

    def top_searches(self, limit: int = 5) -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT query, COUNT(*) AS cnt FROM user_search_history
                WHERE searched_at > DATE_SUB(NOW(), INTERVAL 30 DAY)
                GROUP BY query ORDER BY cnt DESC LIMIT %s
                """,
                (limit,),
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def check_rate_limit(self, telegram_id: int, action: str, max_count: int, seconds: int) -> bool:
        """Return True if allowed, False if rate limited."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT COUNT(*) FROM rate_limits
                   WHERE telegram_id = %s AND action = %s
                   AND created_at > DATE_SUB(NOW(), INTERVAL %s SECOND)""",
                (telegram_id, action, seconds),
            )
            count = cursor.fetchone()[0]
            if count >= max_count:
                return False
            cursor.execute(
                "INSERT INTO rate_limits (telegram_id, action) VALUES (%s, %s)",
                (telegram_id, action),
            )
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            return True
        finally:
            conn.close()

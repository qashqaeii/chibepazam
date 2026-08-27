from database.connection import get_connection


class CookedRepository:
    def mark_cooked(self, user_id: int, recipe_id: int) -> int:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO user_cooked_recipes (user_id, recipe_id, cook_count, last_cooked_at)
                VALUES (%s, %s, 1, NOW())
                ON DUPLICATE KEY UPDATE cook_count = cook_count + 1, last_cooked_at = NOW()
                """,
                (user_id, recipe_id),
            )
            conn.commit()
            cursor.execute(
                "SELECT cook_count FROM user_cooked_recipes WHERE user_id = %s AND recipe_id = %s",
                (user_id, recipe_id),
            )
            row = cursor.fetchone()
            return int(row[0]) if row else 1
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def count_for_user(self, user_id: int) -> int:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COALESCE(SUM(cook_count), 0) FROM user_cooked_recipes WHERE user_id = %s",
                (user_id,),
            )
            return int(cursor.fetchone()[0])
        finally:
            conn.close()

    def distinct_count(self, user_id: int) -> int:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM user_cooked_recipes WHERE user_id = %s",
                (user_id,),
            )
            return int(cursor.fetchone()[0])
        finally:
            conn.close()

    def count_all(self) -> int:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COALESCE(SUM(cook_count), 0) FROM user_cooked_recipes")
            return int(cursor.fetchone()[0])
        finally:
            conn.close()

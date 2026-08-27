from database.connection import get_connection

RATING_SCORE = {"love": 5.0, "good": 4.0, "ok": 3.0, "bad": 1.0}


class RatingsRepository:
    def get_user_rating(self, user_id: int, recipe_id: int) -> str | None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT rating FROM recipe_ratings WHERE user_id = %s AND recipe_id = %s",
                (user_id, recipe_id),
            )
            row = cursor.fetchone()
            return row[0] if row else None
        finally:
            conn.close()

    def set_rating(self, user_id: int, recipe_id: int, rating: str) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO recipe_ratings (user_id, recipe_id, rating)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE rating = VALUES(rating), updated_at = NOW()
                """,
                (user_id, recipe_id, rating),
            )
            self._refresh_recipe_aggregate(cursor, recipe_id)
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _refresh_recipe_aggregate(self, cursor, recipe_id: int) -> None:
        cursor.execute(
            """
            SELECT COUNT(*),
                   AVG(CASE rating
                       WHEN 'love' THEN 5 WHEN 'good' THEN 4 WHEN 'ok' THEN 3 ELSE 1 END)
            FROM recipe_ratings WHERE recipe_id = %s
            """,
            (recipe_id,),
        )
        count, avg = cursor.fetchone()
        cursor.execute(
            "UPDATE recipes SET rating = %s, rating_count = %s WHERE id = %s",
            (round(float(avg or 4.0), 1), int(count or 0), recipe_id),
        )

    def get_aggregate(self, recipe_id: int) -> tuple[float, int]:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT rating, rating_count FROM recipes WHERE id = %s",
                (recipe_id,),
            )
            row = cursor.fetchone()
            if not row:
                return 4.0, 0
            return float(row[0] or 4.0), int(row[1] or 0)
        finally:
            conn.close()

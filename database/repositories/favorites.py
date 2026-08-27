from database.connection import get_connection


class FavoritesRepository:
    def add(self, user_id: int, recipe_id: int) -> bool:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT IGNORE INTO user_favorites (user_id, recipe_id)
                   VALUES (%s, %s)""",
                (user_id, recipe_id),
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def remove(self, user_id: int, recipe_id: int) -> bool:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM user_favorites WHERE user_id = %s AND recipe_id = %s",
                (user_id, recipe_id),
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def is_favorite(self, user_id: int, recipe_id: int) -> bool:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM user_favorites WHERE user_id = %s AND recipe_id = %s LIMIT 1",
                (user_id, recipe_id),
            )
            return cursor.fetchone() is not None
        finally:
            conn.close()

    def get_all(self, user_id: int) -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """SELECT r.*, uf.created_at AS favorited_at
                   FROM user_favorites uf
                   JOIN recipes r ON r.id = uf.recipe_id
                   WHERE uf.user_id = %s AND r.is_active = 1
                   ORDER BY uf.created_at DESC""",
                (user_id,),
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def count_popular(self, limit: int = 10) -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """SELECT r.id, r.name, r.emoji, COUNT(uf.id) AS fav_count
                   FROM user_favorites uf
                   JOIN recipes r ON r.id = uf.recipe_id
                   GROUP BY r.id, r.name, r.emoji
                   ORDER BY fav_count DESC
                   LIMIT %s""",
                (limit,),
            )
            return cursor.fetchall()
        finally:
            conn.close()

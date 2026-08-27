from database.connection import get_connection


class DislikesRepository:
    def get_ids(self, user_id: int) -> set[int]:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT recipe_id FROM user_disliked_recipes WHERE user_id = %s",
                (user_id,),
            )
            return {row[0] for row in cursor.fetchall()}
        finally:
            conn.close()

    def toggle(self, user_id: int, recipe_id: int) -> bool:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM user_disliked_recipes WHERE user_id = %s AND recipe_id = %s",
                (user_id, recipe_id),
            )
            if cursor.fetchone():
                cursor.execute(
                    "DELETE FROM user_disliked_recipes WHERE user_id = %s AND recipe_id = %s",
                    (user_id, recipe_id),
                )
                conn.commit()
                return False
            cursor.execute(
                "INSERT INTO user_disliked_recipes (user_id, recipe_id) VALUES (%s, %s)",
                (user_id, recipe_id),
            )
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def is_disliked(self, user_id: int, recipe_id: int) -> bool:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM user_disliked_recipes WHERE user_id = %s AND recipe_id = %s LIMIT 1",
                (user_id, recipe_id),
            )
            return cursor.fetchone() is not None
        finally:
            conn.close()

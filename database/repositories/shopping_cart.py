from database.connection import get_connection


class ShoppingCartRepository:
    def get_recipe_ids(self, user_id: int) -> list[int]:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT recipe_id FROM user_shopping_cart WHERE user_id = %s ORDER BY created_at",
                (user_id,),
            )
            return [row[0] for row in cursor.fetchall()]
        finally:
            conn.close()

    def add(self, user_id: int, recipe_id: int) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT IGNORE INTO user_shopping_cart (user_id, recipe_id) VALUES (%s, %s)
                """,
                (user_id, recipe_id),
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def remove(self, user_id: int, recipe_id: int) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM user_shopping_cart WHERE user_id = %s AND recipe_id = %s",
                (user_id, recipe_id),
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def clear(self, user_id: int) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user_shopping_cart WHERE user_id = %s", (user_id,))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def count(self, user_id: int) -> int:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM user_shopping_cart WHERE user_id = %s",
                (user_id,),
            )
            return int(cursor.fetchone()[0])
        finally:
            conn.close()

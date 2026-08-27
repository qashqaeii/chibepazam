from database.connection import get_connection


class RecipeCategoriesRepository:
    def get_all(self) -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM recipe_categories ORDER BY sort_order, id"
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def toggle_active(self, category_id: int) -> bool:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE recipe_categories SET is_active = NOT is_active WHERE id = %s",
                (category_id,),
            )
            conn.commit()
            cursor.execute(
                "SELECT is_active FROM recipe_categories WHERE id = %s",
                (category_id,),
            )
            row = cursor.fetchone()
            return bool(row[0]) if row else False
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

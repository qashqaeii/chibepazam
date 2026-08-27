from database.connection import get_connection


class SubstitutesRepository:
    def get_for_ingredient(self, ingredient_id: int) -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT s.*, i.name, i.emoji, i.slug
                FROM ingredient_substitutes s
                JOIN ingredients i ON i.id = s.substitute_ingredient_id
                WHERE s.ingredient_id = %s AND s.is_active = 1 AND i.is_active = 1
                ORDER BY i.name
                """,
                (ingredient_id,),
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def get_for_recipe(self, recipe_id: int) -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT DISTINCT s.ingredient_id, s.substitute_ingredient_id, s.note,
                       i1.name AS ingredient_name, i1.emoji AS ingredient_emoji,
                       i2.name AS substitute_name, i2.emoji AS substitute_emoji
                FROM recipe_ingredients ri
                JOIN ingredient_substitutes s ON s.ingredient_id = ri.ingredient_id AND s.is_active = 1
                JOIN ingredients i1 ON i1.id = s.ingredient_id
                JOIN ingredients i2 ON i2.id = s.substitute_ingredient_id AND i2.is_active = 1
                WHERE ri.recipe_id = %s
                ORDER BY i1.name, i2.name
                """,
                (recipe_id,),
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def list_all(self, limit: int = 100) -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT s.*, i1.name AS from_name, i2.name AS to_name
                FROM ingredient_substitutes s
                JOIN ingredients i1 ON i1.id = s.ingredient_id
                JOIN ingredients i2 ON i2.id = s.substitute_ingredient_id
                ORDER BY s.id DESC LIMIT %s
                """,
                (limit,),
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def add(self, ingredient_id: int, substitute_id: int, note: str | None = None) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO ingredient_substitutes (ingredient_id, substitute_ingredient_id, note)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE note = VALUES(note), is_active = 1
                """,
                (ingredient_id, substitute_id, note),
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def deactivate(self, sub_id: int) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE ingredient_substitutes SET is_active = 0 WHERE id = %s",
                (sub_id,),
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

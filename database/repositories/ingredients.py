from database.connection import get_connection


class IngredientsRepository:
    def get_categories(self) -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """SELECT * FROM ingredient_categories
                   WHERE is_active = 1 ORDER BY sort_order, id"""
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def get_category(self, category_id: int) -> dict | None:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM ingredient_categories WHERE id = %s AND is_active = 1",
                (category_id,),
            )
            return cursor.fetchone()
        finally:
            conn.close()

    def get_by_category(self, category_id: int) -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """SELECT * FROM ingredients
                   WHERE category_id = %s AND is_active = 1
                   ORDER BY sort_order, name""",
                (category_id,),
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def get_by_id(self, ingredient_id: int) -> dict | None:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT i.*, c.name AS category_name, c.emoji AS category_emoji "
                "FROM ingredients i "
                "JOIN ingredient_categories c ON c.id = i.category_id "
                "WHERE i.id = %s AND i.is_active = 1",
                (ingredient_id,),
            )
            return cursor.fetchone()
        finally:
            conn.close()

    def get_by_ids(self, ingredient_ids: list[int]) -> list[dict]:
        if not ingredient_ids:
            return []
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            placeholders = ",".join(["%s"] * len(ingredient_ids))
            cursor.execute(
                f"SELECT * FROM ingredients WHERE id IN ({placeholders}) AND is_active = 1",
                tuple(ingredient_ids),
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def count_all(self) -> int:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM ingredients WHERE is_active = 1")
            return cursor.fetchone()[0]
        finally:
            conn.close()

    def get_common_ingredients(self) -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM ingredients WHERE is_common = 1 AND is_active = 1 ORDER BY sort_order"
            )
            return cursor.fetchall()
        finally:
            conn.close()

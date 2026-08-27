from database.connection import get_connection


class IngredientsRepository:
    def get_categories(self) -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """SELECT c.*, COUNT(i.id) AS item_count
                   FROM ingredient_categories c
                   LEFT JOIN ingredients i
                     ON i.category_id = c.id AND i.is_active = 1
                   WHERE c.is_active = 1
                   GROUP BY c.id
                   ORDER BY c.sort_order, c.id"""
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

    def get_all_active(self) -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM ingredients WHERE is_active = 1 ORDER BY name"
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def toggle_active(self, ingredient_id: int) -> bool:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE ingredients SET is_active = NOT is_active WHERE id = %s",
                (ingredient_id,),
            )
            conn.commit()
            cursor.execute("SELECT is_active FROM ingredients WHERE id = %s", (ingredient_id,))
            row = cursor.fetchone()
            return bool(row[0]) if row else False
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def list_page(self, page: int = 1, per_page: int = 20) -> tuple[list[dict], int, int]:
        from utils.pagination import paginate

        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM ingredients ORDER BY is_active DESC, name")
            rows = cursor.fetchall()
            return paginate(rows, page, per_page)
        finally:
            conn.close()

    def get_common_ingredients(self) -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT i.* FROM ingredients i "
                "JOIN ingredient_categories c ON c.id = i.category_id "
                "WHERE i.is_common = 1 AND i.is_active = 1 "
                "ORDER BY c.sort_order, i.sort_order, i.name"
            )
            return cursor.fetchall()
        finally:
            conn.close()

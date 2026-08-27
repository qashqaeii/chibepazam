from database.connection import get_connection


class PantryRepository:
    def get_user_ingredient_ids(self, user_id: int) -> set[int]:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT ingredient_id FROM user_pantry WHERE user_id = %s",
                (user_id,),
            )
            return {row[0] for row in cursor.fetchall()}
        finally:
            conn.close()

    def toggle(self, user_id: int, ingredient_id: int) -> bool:
        """Toggle ingredient. Returns True if added, False if removed."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM user_pantry WHERE user_id = %s AND ingredient_id = %s",
                (user_id, ingredient_id),
            )
            exists = cursor.fetchone()
            if exists:
                cursor.execute(
                    "DELETE FROM user_pantry WHERE user_id = %s AND ingredient_id = %s",
                    (user_id, ingredient_id),
                )
                conn.commit()
                return False
            cursor.execute(
                "INSERT INTO user_pantry (user_id, ingredient_id) VALUES (%s, %s)",
                (user_id, ingredient_id),
            )
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def clear(self, user_id: int) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user_pantry WHERE user_id = %s", (user_id,))
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
                "SELECT COUNT(*) FROM user_pantry WHERE user_id = %s",
                (user_id,),
            )
            return cursor.fetchone()[0]
        finally:
            conn.close()

    def get_permanent_ids(self, user_id: int) -> set[int]:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT ingredient_id FROM user_permanent_ingredients WHERE user_id = %s",
                (user_id,),
            )
            return {row[0] for row in cursor.fetchall()}
        finally:
            conn.close()

    def toggle_permanent(self, user_id: int, ingredient_id: int) -> bool:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id FROM user_permanent_ingredients
                   WHERE user_id = %s AND ingredient_id = %s""",
                (user_id, ingredient_id),
            )
            exists = cursor.fetchone()
            if exists:
                cursor.execute(
                    """DELETE FROM user_permanent_ingredients
                       WHERE user_id = %s AND ingredient_id = %s""",
                    (user_id, ingredient_id),
                )
                conn.commit()
                return False
            cursor.execute(
                """INSERT INTO user_permanent_ingredients (user_id, ingredient_id)
                   VALUES (%s, %s)""",
                (user_id, ingredient_id),
            )
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_combined_ids(self, user_id: int) -> set[int]:
        pantry = self.get_user_ingredient_ids(user_id)
        permanent = self.get_permanent_ids(user_id)
        return pantry | permanent

from database.connection import get_connection


class SettingsRepository:
    def get(self, user_id: int) -> dict | None:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM user_settings WHERE user_id = %s",
                (user_id,),
            )
            return cursor.fetchone()
        finally:
            conn.close()

    def update_servings(self, user_id: int, servings: int) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE user_settings SET servings = %s WHERE user_id = %s",
                (servings, user_id),
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def update_diet(self, user_id: int, diet_type: str) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE user_settings SET diet_type = %s WHERE user_id = %s",
                (diet_type, user_id),
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def toggle_notifications(self, user_id: int) -> bool:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT notifications FROM user_settings WHERE user_id = %s",
                (user_id,),
            )
            row = cursor.fetchone()
            new_val = 0 if row and row["notifications"] else 1
            cursor.execute(
                "UPDATE user_settings SET notifications = %s WHERE user_id = %s",
                (new_val, user_id),
            )
            conn.commit()
            return bool(new_val)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_forbidden_ids(self, user_id: int) -> set[int]:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT ingredient_id FROM user_forbidden_ingredients WHERE user_id = %s",
                (user_id,),
            )
            return {row[0] for row in cursor.fetchall()}
        finally:
            conn.close()

    def toggle_forbidden(self, user_id: int, ingredient_id: int) -> bool:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id FROM user_forbidden_ingredients
                   WHERE user_id = %s AND ingredient_id = %s""",
                (user_id, ingredient_id),
            )
            exists = cursor.fetchone()
            if exists:
                cursor.execute(
                    """DELETE FROM user_forbidden_ingredients
                       WHERE user_id = %s AND ingredient_id = %s""",
                    (user_id, ingredient_id),
                )
                conn.commit()
                return False
            cursor.execute(
                """INSERT INTO user_forbidden_ingredients (user_id, ingredient_id)
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

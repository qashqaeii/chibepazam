from database.connection import get_connection


class RecipesRepository:
    def get_by_id(self, recipe_id: int) -> dict | None:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """SELECT r.*, rc.name AS category_name
                   FROM recipes r
                   LEFT JOIN recipe_categories rc ON rc.id = r.category_id
                   WHERE r.id = %s AND r.is_active = 1""",
                (recipe_id,),
            )
            return cursor.fetchone()
        finally:
            conn.close()

    def get_ingredients(self, recipe_id: int) -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """SELECT ri.*, i.name, i.slug, i.emoji, i.is_common
                   FROM recipe_ingredients ri
                   JOIN ingredients i ON i.id = ri.ingredient_id
                   WHERE ri.recipe_id = %s
                   ORDER BY ri.importance DESC, i.name""",
                (recipe_id,),
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def get_all_active(self) -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM recipes WHERE is_active = 1 ORDER BY name"
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def search(self, query: str, limit: int = 20) -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            like = f"%{query}%"
            cursor.execute(
                """SELECT DISTINCT r.* FROM recipes r
                   LEFT JOIN recipe_ingredients ri ON ri.recipe_id = r.id
                   LEFT JOIN ingredients i ON i.id = ri.ingredient_id
                   WHERE r.is_active = 1
                   AND (r.name LIKE %s OR i.name LIKE %s)
                   LIMIT %s""",
                (like, like, limit),
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def get_random(
        self,
        difficulty: str | None = None,
        cost_level: str | None = None,
        is_vegetarian: bool | None = None,
        exclude_ids: list[int] | None = None,
    ) -> dict | None:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            conditions = ["is_active = 1"]
            params: list = []

            if difficulty:
                conditions.append("difficulty = %s")
                params.append(difficulty)
            if cost_level:
                conditions.append("cost_level = %s")
                params.append(cost_level)
            if is_vegetarian is not None:
                conditions.append("is_vegetarian = %s")
                params.append(1 if is_vegetarian else 0)
            if exclude_ids:
                placeholders = ",".join(["%s"] * len(exclude_ids))
                conditions.append(f"id NOT IN ({placeholders})")
                params.extend(exclude_ids)

            where = " AND ".join(conditions)
            cursor.execute(
                f"SELECT * FROM recipes WHERE {where} ORDER BY RAND() LIMIT 1",
                tuple(params),
            )
            return cursor.fetchone()
        finally:
            conn.close()

    def count_all(self) -> int:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM recipes WHERE is_active = 1")
            return cursor.fetchone()[0]
        finally:
            conn.close()

    def get_similar(self, recipe_id: int, limit: int = 3) -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """SELECT r2.* FROM recipes r2
                   JOIN recipe_ingredients ri1 ON ri1.recipe_id = %s
                   JOIN recipe_ingredients ri2 ON ri2.ingredient_id = ri1.ingredient_id
                   WHERE r2.id = ri2.recipe_id AND r2.id != %s AND r2.is_active = 1
                   GROUP BY r2.id
                   ORDER BY COUNT(*) DESC
                   LIMIT %s""",
                (recipe_id, recipe_id, limit),
            )
            return cursor.fetchall()
        finally:
            conn.close()

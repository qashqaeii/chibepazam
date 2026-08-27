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
                """SELECT r.*, rc.slug AS category_slug
                   FROM recipes r
                   LEFT JOIN recipe_categories rc ON rc.id = r.category_id
                   WHERE r.is_active = 1 ORDER BY r.name"""
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def search(self, query: str, limit: int = 20) -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            q = query.strip()
            if len(q) < 2:
                return []
            try:
                cursor.execute(
                    """
                    SELECT DISTINCT r.* FROM recipes r
                    LEFT JOIN recipe_ingredients ri ON ri.recipe_id = r.id
                    LEFT JOIN ingredients i ON i.id = ri.ingredient_id
                    WHERE r.is_active = 1 AND (
                        MATCH(r.name, r.description) AGAINST (%s IN NATURAL LANGUAGE MODE)
                        OR r.name LIKE %s OR i.name LIKE %s
                    )
                    LIMIT %s
                    """,
                    (q, f"%{q}%", f"%{q}%", limit),
                )
                rows = cursor.fetchall()
                if rows:
                    return rows
            except Exception:
                pass
            like = f"%{q}%"
            cursor.execute(
                """SELECT DISTINCT r.* FROM recipes r
                   LEFT JOIN recipe_ingredients ri ON ri.recipe_id = r.id
                   LEFT JOIN ingredients i ON i.id = ri.ingredient_id
                   WHERE r.is_active = 1
                   AND (r.name LIKE %s OR r.description LIKE %s OR i.name LIKE %s)
                   LIMIT %s""",
                (like, like, like, limit),
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
        max_total_time: int | None = None,
        require_any_slugs: list[str] | None = None,
        require_category_slugs: list[str] | None = None,
    ) -> dict | None:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            conditions = ["r.is_active = 1"]
            params: list = []

            if difficulty:
                conditions.append("r.difficulty = %s")
                params.append(difficulty)
            if cost_level:
                conditions.append("r.cost_level = %s")
                params.append(cost_level)
            if is_vegetarian is not None:
                conditions.append("r.is_vegetarian = %s")
                params.append(1 if is_vegetarian else 0)
            if max_total_time is not None:
                conditions.append("(r.prep_time + r.cook_time) <= %s")
                params.append(max_total_time)
            if exclude_ids:
                placeholders = ",".join(["%s"] * len(exclude_ids))
                conditions.append(f"r.id NOT IN ({placeholders})")
                params.extend(exclude_ids)
            if require_any_slugs:
                placeholders = ",".join(["%s"] * len(require_any_slugs))
                conditions.append(
                    f"""EXISTS (
                        SELECT 1 FROM recipe_ingredients ri
                        JOIN ingredients i ON i.id = ri.ingredient_id
                        WHERE ri.recipe_id = r.id AND i.slug IN ({placeholders})
                    )"""
                )
                params.extend(require_any_slugs)
            if require_category_slugs:
                placeholders = ",".join(["%s"] * len(require_category_slugs))
                conditions.append(
                    f"""r.category_id IN (
                        SELECT id FROM recipe_categories WHERE slug IN ({placeholders})
                    )"""
                )
                params.extend(require_category_slugs)

            where = " AND ".join(conditions)
            cursor.execute(
                f"SELECT r.* FROM recipes r WHERE {where} ORDER BY RAND() LIMIT 1",
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
                   JOIN recipe_ingredients ri1
                     ON ri1.recipe_id = %s AND ri1.importance >= 5
                   JOIN ingredients i
                     ON i.id = ri1.ingredient_id AND i.is_common = 0
                   JOIN recipe_ingredients ri2
                     ON ri2.ingredient_id = ri1.ingredient_id AND ri2.importance >= 5
                   WHERE r2.id = ri2.recipe_id AND r2.id != %s AND r2.is_active = 1
                   GROUP BY r2.id
                   ORDER BY COUNT(*) DESC
                   LIMIT %s""",
                (recipe_id, recipe_id, limit),
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def toggle_active(self, recipe_id: int) -> bool:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE recipes SET is_active = NOT is_active WHERE id = %s",
                (recipe_id,),
            )
            conn.commit()
            cursor.execute("SELECT is_active FROM recipes WHERE id = %s", (recipe_id,))
            row = cursor.fetchone()
            return bool(row[0]) if row else False
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def list_page(self, page: int = 1, per_page: int = 15) -> tuple[list[dict], int, int]:
        from utils.pagination import paginate

        all_recipes = self.get_all_active() + self._get_inactive()
        return paginate(all_recipes, page, per_page)

    def _get_inactive(self) -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """SELECT r.*, rc.slug AS category_slug
                   FROM recipes r
                   LEFT JOIN recipe_categories rc ON rc.id = r.category_id
                   WHERE r.is_active = 0 ORDER BY r.name"""
            )
            return cursor.fetchall()
        finally:
            conn.close()

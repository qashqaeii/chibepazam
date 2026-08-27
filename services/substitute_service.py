from database.repositories.substitutes import SubstitutesRepository


class SubstituteService:
    def __init__(self):
        self.repo = SubstitutesRepository()

    def for_recipe(self, recipe_id: int) -> list[dict]:
        return self.repo.get_for_recipe(recipe_id)

    def format_lines(self, recipe_id: int) -> list[str]:
        rows = self.for_recipe(recipe_id)
        if not rows:
            return []
        lines = []
        current = None
        for row in rows:
            key = row["ingredient_id"]
            if key != current:
                current = key
                lines.append(f"{row['ingredient_emoji']} {row['ingredient_name']}:")
            note = f" ({row['note']})" if row.get("note") else ""
            lines.append(f"  ↳ {row['substitute_emoji']} {row['substitute_name']}{note}")
        return lines

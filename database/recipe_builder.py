"""Helpers for canonical recipe seed records."""

_OPT = dict(required=False, optional=True)


def _ing(ingredient_id, amount, unit, importance, required=True, optional=False):
    return {
        "ingredient_id": ingredient_id,
        "amount": amount,
        "unit": unit,
        "importance": importance,
        "is_required": 1 if required else 0,
        "is_optional": 1 if optional else 0,
    }

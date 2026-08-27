"""Build share text/URL for recipes."""

from urllib.parse import quote

from utils.telegram import difficulty_label


def build_recipe_share_text(recipe: dict, bot_username: str = "Chibepazamrobot") -> str:
    total = recipe.get("prep_time", 0) + recipe.get("cook_time", 0)
    diff = difficulty_label(recipe.get("difficulty", "medium"))
    name = recipe.get("name", "غذا")
    username = bot_username.lstrip("@")
    return (
        f"🍲 {name}\n"
        f"⏱ {total} دقیقه  ·  {diff}\n\n"
        f"@{username}"
    )


def build_recipe_share_url(recipe: dict, bot_username: str) -> str | None:
    text = build_recipe_share_text(recipe, bot_username)
    username = bot_username.lstrip("@")
    bot_url = f"https://t.me/{username}"
    url = f"https://t.me/share/url?url={quote(bot_url, safe='')}&text={quote(text, safe='')}"
    if len(url) > 2000:
        return None
    return url

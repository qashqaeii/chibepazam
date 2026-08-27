def paginate(items: list, page: int, per_page: int) -> tuple[list, int, int]:
    """Return (page_items, current_page, total_pages). page is 1-based."""
    if not items:
        return [], 1, 1
    total_pages = max(1, (len(items) + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    return items[start : start + per_page], page, total_pages

"""Format and paginate cooking instructions for Telegram."""

MAX_STEP_PAGE_CHARS = 1600


def format_instructions(text: str) -> str:
    lines: list[str] = []
    for raw in str(text).splitlines():
        line = raw.strip()
        if not line:
            if lines and lines[-1] != "":
                lines.append("")
            continue
        numbered = line[0].isdigit() and ". " in line[:4]
        if numbered and lines and lines[-1] != "":
            lines.append("")
        lines.append(line)
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def paginate_instructions(text: str, page: int = 1, max_chars: int = MAX_STEP_PAGE_CHARS) -> tuple[str, int, int]:
    formatted = format_instructions(text)
    chunks = [p.strip() for p in formatted.split("\n\n") if p.strip()]
    if not chunks:
        return formatted, 1, 1

    pages: list[str] = []
    buf: list[str] = []
    size = 0
    for chunk in chunks:
        extra = len(chunk) + (2 if buf else 0)
        if buf and size + extra > max_chars:
            pages.append("\n\n".join(buf))
            buf = [chunk]
            size = len(chunk)
        else:
            buf.append(chunk)
            size += extra
    if buf:
        pages.append("\n\n".join(buf))

    total = len(pages)
    page = max(1, min(page, total))
    return pages[page - 1], page, total

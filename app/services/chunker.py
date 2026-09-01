def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150) -> list[str]:
    normalized = text.replace("\r\n", "\n").strip()
    if not normalized:
        return []

    chunks: list[str] = []
    start = 0
    length = len(normalized)

    while start < length:
        end = min(start + chunk_size, length)
        if end < length:
            break_at = _best_break(normalized, start, end)
            if break_at > start:
                end = break_at

        chunk = normalized[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= length:
            break
        start = max(end - overlap, start + 1)

    return chunks


def _best_break(text: str, start: int, end: int) -> int:
    window = text[start:end]
    for separator in ("\n\n", "\n", ". ", " "):
        index = window.rfind(separator)
        if index != -1 and index > len(window) * 0.4:
            return start + index + len(separator)
    return end

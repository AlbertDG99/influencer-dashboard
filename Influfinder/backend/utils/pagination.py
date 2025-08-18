from __future__ import annotations

from typing import Any, Dict, List


def paginate(items: List[dict], *, page: int, page_size: int) -> Dict[str, Any]:
    """Return a paginated slice with metadata.

    Args:
        items: Full list to paginate (already filtered/sorted).
        page: 1-based page index.
        page_size: number of items per page.

    Returns:
        Dict with items, page, page_size, total, total_pages
    """
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    page_items = items[start:end]
    total_pages = (total + page_size - 1) // page_size if page_size > 0 else 1
    return {
        "items": page_items,
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
    }


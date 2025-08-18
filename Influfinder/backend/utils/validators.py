from __future__ import annotations

from typing import Tuple

from flask import Request


CATEGORIES = {
    "fitness",
    "fashion",
    "travel",
    "food",
    "tech",
    "business",
    "lifestyle",
    "gaming",
}


def sanitize_hashtag(tag: str) -> str:
    return tag.lstrip("#").strip()


def parse_pagination(request: Request) -> Tuple[int, int]:
    page = request.args.get("page", default="1")
    page_size = request.args.get("page_size", default="20")
    try:
        p = max(1, int(page))
    except ValueError:
        p = 1
    try:
        ps = max(1, min(100, int(page_size)))
    except ValueError:
        ps = 20
    return p, ps


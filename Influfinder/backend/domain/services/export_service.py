from __future__ import annotations

import csv
import io
from typing import Optional

from openpyxl import Workbook

from backend.domain.repositories.base import InfluencerRepository
from backend.utils.pagination import paginate


_HEADERS = [
    "id",
    "username",
    "full_name",
    "followers",
    "following",
    "posts",
    "engagement_rate",
    "categories",
    "languages",
    "hashtags",
]


class ExportService:
    """Service to export influencer data into CSV and XLSX."""

    def __init__(self, repository: InfluencerRepository) -> None:
        self._repository = repository

    def _query(self, *, query: Optional[str], category: Optional[str]) -> list[dict]:
        items = [i.to_dict() for i in self._repository.search(query=query, category=category)]
        return items

    def export_csv(self, *, query: Optional[str], category: Optional[str], page: int, page_size: int) -> bytes:
        data = paginate(self._query(query=query, category=category), page=page, page_size=page_size)["items"]
        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=_HEADERS)
        writer.writeheader()
        for row in data:
            writer.writerow({
                "id": row["id"],
                "username": row["username"],
                "full_name": row["full_name"],
                "followers": row["followers"],
                "following": row["following"],
                "posts": row["posts"],
                "engagement_rate": row["engagement_rate"],
                "categories": ",".join(row.get("categories", [])),
                "languages": ",".join(row.get("languages", [])),
                "hashtags": ",".join(row.get("hashtags", [])),
            })
        return buffer.getvalue().encode("utf-8")

    def export_xlsx(self, *, query: Optional[str], category: Optional[str], page: int, page_size: int) -> bytes:
        data = paginate(self._query(query=query, category=category), page=page, page_size=page_size)["items"]
        wb = Workbook()
        ws = wb.active
        ws.title = "Influencers"
        ws.append(_HEADERS)
        for row in data:
            ws.append([
                row["id"],
                row["username"],
                row["full_name"],
                row["followers"],
                row["following"],
                row["posts"],
                row["engagement_rate"],
                ",".join(row.get("categories", [])),
                ",".join(row.get("languages", [])),
                ",".join(row.get("hashtags", [])),
            ])
        stream = io.BytesIO()
        wb.save(stream)
        return stream.getvalue()

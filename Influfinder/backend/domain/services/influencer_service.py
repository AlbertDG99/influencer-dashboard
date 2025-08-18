from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, List, Optional

from backend.domain.repositories.base import InfluencerRepository
from backend.web.errors import NotFoundError, ValidationError
from backend.utils.pagination import paginate
from backend.utils.validators import CATEGORIES, sanitize_hashtag


class InfluencerService:
    """Service layer for influencer business logic."""

    def __init__(self, repository: InfluencerRepository) -> None:
        self._repository = repository

    def get_by_id(self, influencer_id: str) -> Dict[str, Any]:
        item = self._repository.find_by_id(influencer_id)
        if not item:
            raise NotFoundError(f"Influencer {influencer_id} no encontrado")
        return item.to_dict()

    def search_influencers(
        self,
        *,
        query: Optional[str],
        category: Optional[str],
        page: int,
        page_size: int,
    ) -> Dict[str, Any]:
        if category and category not in CATEGORIES:
            raise ValidationError(f"Categoría inválida: {category}")
        items = [i.to_dict() for i in self._repository.search(query=query, category=category)]
        return paginate(items, page=page, page_size=page_size)

    def search_by_hashtag(self, *, hashtag: str, page: int, page_size: int) -> Dict[str, Any]:
        tag = sanitize_hashtag(hashtag)
        items = [i.to_dict() for i in self._repository.search_by_hashtag(hashtag=tag)]
        return paginate(items, page=page, page_size=page_size)

    def get_trending(self, *, category: Optional[str], page: int, page_size: int) -> Dict[str, Any]:
        if category and category not in CATEGORIES:
            raise ValidationError(f"Categoría inválida: {category}")
        items = [i.to_dict() for i in self._repository.trending(category=category)]
        return paginate(items, page=page, page_size=page_size)

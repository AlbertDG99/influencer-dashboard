from __future__ import annotations

from typing import List, Optional, Protocol

from backend.domain.models.influencer import Influencer


class InfluencerRepository(Protocol):
    """Repository interface for accessing influencer data."""

    def find_by_id(self, influencer_id: str) -> Optional[Influencer]:
        ...

    def search(self, *, query: Optional[str], category: Optional[str]) -> List[Influencer]:
        ...

    def search_by_hashtag(self, *, hashtag: str) -> List[Influencer]:
        ...

    def trending(self, *, category: Optional[str]) -> List[Influencer]:
        ...

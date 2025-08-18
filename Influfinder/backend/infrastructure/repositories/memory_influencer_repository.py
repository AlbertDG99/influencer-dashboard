from __future__ import annotations

import re
from typing import List, Optional

from backend.domain.models.influencer import Influencer
from backend.domain.repositories.base import InfluencerRepository


_SAMPLE_DATA: List[Influencer] = [
    Influencer(
        id="1",
        username="fit_maria",
        full_name="María López",
        bio="Entrenadora personal y nutrición",
        followers=250000,
        following=350,
        posts=1200,
        engagement_rate=0.045,
        categories=["fitness", "lifestyle"],
        languages=["es"],
        hashtags=["fitness", "salud", "gym"],
        avatar_url="https://i.pravatar.cc/150?img=1",
    ),
    Influencer(
        id="2",
        username="tech_guru",
        full_name="John Smith",
        bio="Gadgets, reviews and tutorials",
        followers=540000,
        following=120,
        posts=980,
        engagement_rate=0.038,
        categories=["tech", "gaming"],
        languages=["en"],
        hashtags=["tech", "gadgets", "gaming"],
        avatar_url="https://i.pravatar.cc/150?img=2",
    ),
    Influencer(
        id="3",
        username="taste_travel",
        full_name="Lucía Pérez",
        bio="Comida y viajes por el mundo",
        followers=420000,
        following=500,
        posts=1500,
        engagement_rate=0.051,
        categories=["travel", "food"],
        languages=["es", "en"],
        hashtags=["viajes", "food", "travel"],
        avatar_url="https://i.pravatar.cc/150?img=3",
    ),
    Influencer(
        id="4",
        username="style_anna",
        full_name="Anna Miller",
        bio="Fashion and lifestyle tips",
        followers=310000,
        following=260,
        posts=800,
        engagement_rate=0.042,
        categories=["fashion", "lifestyle"],
        languages=["en"],
        hashtags=["fashion", "outfit", "style"],
        avatar_url="https://i.pravatar.cc/150?img=4",
    ),
    Influencer(
        id="5",
        username="biz_mindset",
        full_name="Carlos Gómez",
        bio="Negocios y productividad",
        followers=280000,
        following=180,
        posts=600,
        engagement_rate=0.033,
        categories=["business", "tech"],
        languages=["es"],
        hashtags=["negocios", "emprendimiento", "productividad"],
        avatar_url="https://i.pravatar.cc/150?img=5",
    ),
    Influencer(
        id="6",
        username="game_arena",
        full_name="Gamer Pro",
        bio="Streaming y e-sports",
        followers=670000,
        following=90,
        posts=2000,
        engagement_rate=0.057,
        categories=["gaming"],
        languages=["es", "en"],
        hashtags=["gaming", "esports", "stream"],
        avatar_url="https://i.pravatar.cc/150?img=6",
    ),
]


class InMemoryInfluencerRepository(InfluencerRepository):
    def __init__(self, data: Optional[List[Influencer]] = None) -> None:
        self._data = list(data) if data is not None else list(_SAMPLE_DATA)

    def find_by_id(self, influencer_id: str) -> Optional[Influencer]:
        for item in self._data:
            if item.id == influencer_id:
                return item
        return None

    def search(self, *, query: Optional[str], category: Optional[str]) -> List[Influencer]:
        results = self._data
        if query:
            q = query.lower()
            results = [i for i in results if q in i.username.lower() or q in i.full_name.lower() or q in i.bio.lower()]
        if category:
            results = [i for i in results if category.lower() in (c.lower() for c in i.categories)]
        return sorted(results, key=lambda i: (i.followers, i.engagement_rate), reverse=True)

    def search_by_hashtag(self, *, hashtag: str) -> List[Influencer]:
        tag = hashtag.lstrip("#").lower()
        return sorted([i for i in self._data if tag in (h.lower() for h in i.hashtags)], key=lambda i: i.engagement_rate, reverse=True)

    def trending(self, *, category: Optional[str]) -> List[Influencer]:
        results = self.search(query=None, category=category)
        return sorted(results, key=lambda i: i.engagement_rate, reverse=True)

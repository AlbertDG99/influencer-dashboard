from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import List, Optional


@dataclass
class Influencer:
    """Domain model representing an Instagram influencer."""

    id: str
    username: str
    full_name: str
    bio: str
    followers: int
    following: int
    posts: int
    engagement_rate: float
    categories: List[str] = field(default_factory=list)
    languages: List[str] = field(default_factory=list)
    hashtags: List[str] = field(default_factory=list)
    avatar_url: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

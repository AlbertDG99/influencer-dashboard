from __future__ import annotations

from typing import List, Optional

from backend.domain.models.influencer import Influencer
from backend.domain.repositories.base import InfluencerRepository
from backend.domain.services.instagram_api_service import InstagramAPIService


_CATEGORY_TAG = {
    "fitness": "fitness",
    "fashion": "fashion",
    "travel": "travel",
    "food": "food",
    "tech": "technology",
    "business": "business",
    "lifestyle": "lifestyle",
    "gaming": "gaming",
}


class InstagramInfluencerRepository(InfluencerRepository):
    def __init__(self, api_service: InstagramAPIService) -> None:
        self._api = api_service

    def find_by_id(self, influencer_id: str) -> Optional[Influencer]:
        user = self._api.get_user_basic(influencer_id)
        if not user:
            return None
        return Influencer(
            id=influencer_id,
            username=user.get("username", ""),
            full_name=user.get("name", ""),
            bio=user.get("biography", ""),
            followers=int(user.get("followers_count", 0)),
            following=int(user.get("follows_count", 0)),
            posts=int(user.get("media_count", 0)),
            engagement_rate=0.0,
            categories=[],
            languages=[],
            hashtags=[],
            avatar_url=user.get("profile_picture_url"),
        )

    def search(self, *, query: Optional[str], category: Optional[str]) -> List[Influencer]:
        result: List[Influencer] = []
        if query:
            bd = self._api.business_discovery_by_username(query)
            if bd:
                result.append(
                    Influencer(
                        id=bd.get("id", bd.get("username", "")),
                        username=bd.get("username", ""),
                        full_name=bd.get("name", ""),
                        bio=bd.get("biography", ""),
                        followers=int(bd.get("followers_count", 0)),
                        following=int(bd.get("follows_count", 0)),
                        posts=int(bd.get("media_count", 0)),
                        engagement_rate=0.0,
                        categories=[category] if category else [],
                        languages=[],
                        hashtags=[],
                        avatar_url=bd.get("profile_picture_url"),
                    )
                )
        return result

    def _aggregate_media_owners(self, media: list[dict], hashtag: str) -> List[Influencer]:
        owners: dict[str, dict] = {}
        for m in media:
            owner = m.get("owner") or {}
            oid = str(owner.get("id")) if owner else None
            if not oid:
                # Try username if present on media
                username = m.get("username")
                if username:
                    bd = self._api.business_discovery_by_username(username)
                    oid = str(bd.get("id")) if bd and bd.get("id") else None
            if not oid:
                continue
            owners.setdefault(oid, {"posts": 0, "likes": 0, "comments": 0})
            owners[oid]["posts"] += 1
            owners[oid]["likes"] += int(m.get("like_count", 0))
            owners[oid]["comments"] += int(m.get("comments_count", 0))
        influencers: List[Influencer] = []
        for oid in owners.keys():
            try:
                user = self._api.get_user_basic(oid)
            except Exception:
                continue
            if not user:
                continue
            followers = int(user.get("followers_count", 0)) or 1
            engagement = (owners[oid]["likes"] + owners[oid]["comments"]) / followers
            influencers.append(
                Influencer(
                    id=oid,
                    username=user.get("username", ""),
                    full_name=user.get("name", ""),
                    bio=user.get("biography", ""),
                    followers=int(user.get("followers_count", 0)),
                    following=int(user.get("follows_count", 0)),
                    posts=int(user.get("media_count", 0)),
                    engagement_rate=float(round(engagement, 4)),
                    categories=[],
                    languages=[],
                    hashtags=[hashtag],
                    avatar_url=user.get("profile_picture_url"),
                )
            )
        return sorted(influencers, key=lambda i: i.engagement_rate, reverse=True)

    def search_by_hashtag(self, *, hashtag: str) -> List[Influencer]:
        tag_id = self._api.search_hashtag_id(hashtag)
        if not tag_id:
            return []
        media = self._api.get_hashtag_top_media(tag_id)
        if not media:
            media = self._api.get_hashtag_recent_media(tag_id)
        return self._aggregate_media_owners(media, hashtag)

    def trending(self, *, category: Optional[str]) -> List[Influencer]:
        tag = _CATEGORY_TAG.get(category or "", "instagood")
        return self.search_by_hashtag(hashtag=tag)

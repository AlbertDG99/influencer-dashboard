from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

import requests


class InstagramAPIService:
    """Instagram Graph API client for hashtag and user discovery.

    Requires an Instagram Business/Creator account linked to a Facebook Page.
    Environment variables:
        - INSTAGRAM_ACCESS_TOKEN
        - IG_BUSINESS_ACCOUNT_ID (the IG User ID)
        - GRAPH_API_VERSION (default: v19.0)
    """

    def __init__(self, access_token: Optional[str] = None, ig_user_id: Optional[str] = None, version: Optional[str] = None) -> None:
        self._access_token = access_token or os.getenv("INSTAGRAM_ACCESS_TOKEN")
        self._ig_user_id = ig_user_id or os.getenv("IG_BUSINESS_ACCOUNT_ID")
        self._version = version or os.getenv("GRAPH_API_VERSION", "v19.0")
        self._base = f"https://graph.facebook.com/{self._version}"
        if not self._access_token or not self._ig_user_id:
            raise ValueError("Instagram Graph API env not configured: INSTAGRAM_ACCESS_TOKEN and IG_BUSINESS_ACCOUNT_ID are required")

    def _get(self, path: str, params: Optional[dict] = None) -> Dict[str, Any]:
        p = dict(params or {})
        p["access_token"] = self._access_token
        url = f"{self._base}{path}"
        resp = requests.get(url, params=p, timeout=15)
        resp.raise_for_status()
        return resp.json()

    def search_hashtag_id(self, hashtag: str) -> Optional[str]:
        q = hashtag.lstrip('#')
        data = self._get("/ig_hashtag_search", {"user_id": self._ig_user_id, "q": q})
        arr = data.get("data", [])
        return arr[0]["id"] if arr else None

    def get_hashtag_top_media(self, hashtag_id: str) -> List[Dict[str, Any]]:
        fields = "id,caption,like_count,comments_count,media_type,media_url,permalink,owner"
        data = self._get(f"/{hashtag_id}/top_media", {"user_id": self._ig_user_id, "fields": fields})
        return data.get("data", [])

    def get_hashtag_recent_media(self, hashtag_id: str) -> List[Dict[str, Any]]:
        fields = "id,caption,like_count,comments_count,media_type,media_url,permalink,owner"
        data = self._get(f"/{hashtag_id}/recent_media", {"user_id": self._ig_user_id, "fields": fields})
        return data.get("data", [])

    def get_user_basic(self, user_id: str) -> Dict[str, Any]:
        fields = "username,profile_picture_url,biography,followers_count,follows_count,media_count,name"
        return self._get(f"/{user_id}", {"fields": fields})

    def business_discovery_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        fields = (
            "business_discovery.username(%s){username,name,profile_picture_url,biography,followers_count,follows_count,media_count}"
            % username
        )
        data = self._get(f"/{self._ig_user_id}", {"fields": fields})
        return data.get("business_discovery")

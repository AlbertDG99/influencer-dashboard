import os
from typing import Optional

from backend.domain.repositories.base import InfluencerRepository
from backend.infrastructure.repositories.memory_influencer_repository import InMemoryInfluencerRepository
from backend.infrastructure.repositories.instagram_influencer_repository import InstagramInfluencerRepository
from backend.domain.services.instagram_api_service import InstagramAPIService


def get_influencer_repository() -> InfluencerRepository:
    use_api = os.getenv("USE_INSTAGRAM_API", "true").lower() != "false"
    token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    ig_user_id = os.getenv("IG_BUSINESS_ACCOUNT_ID")
    if use_api and token and ig_user_id:
        api = InstagramAPIService(access_token=token, ig_user_id=ig_user_id)
        return InstagramInfluencerRepository(api_service=api)
    return InMemoryInfluencerRepository()


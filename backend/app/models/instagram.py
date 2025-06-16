from pydantic import BaseModel, HttpUrl
from typing import Optional

class InstagramProfile(BaseModel):
    username: str
    full_name: Optional[str] = None
    biography: Optional[str] = None
    followers_count: int
    following_count: int
    profile_pic_url: HttpUrl
    is_private: bool
    is_verified: bool
    media_count: int
    latest_post_url: Optional[HttpUrl] = None 
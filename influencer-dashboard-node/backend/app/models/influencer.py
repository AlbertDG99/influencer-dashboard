import enum
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel, JSON, Column

class InfluencerCategory(str, enum.Enum):
    """
    Enum for influencer categories.
    """
    FASHION = "fashion"
    FITNESS = "fitness"
    FOOD = "food"
    TRAVEL = "travel"
    BEAUTY = "beauty"
    TECHNOLOGY = "technology"
    OTHER = "other"

class PostBase(SQLModel):
    """
    Base model for a post.
    """
    external_id: str = Field(index=True, unique=True)
    caption: Optional[str]
    image_url: str
    metrics: Optional[dict] = Field(default={}, sa_column=Column(JSON))
    
class Post(PostBase, table=True):
    """
    Database model for a post.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    influencer_id: int = Field(foreign_key="influencer.id")
    influencer: "Influencer" = Relationship(back_populates="posts")

class InfluencerBase(SQLModel):
    """
    Base model for an influencer.
    """
    username: str = Field(index=True, unique=True)
    full_name: Optional[str]
    bio: Optional[str]
    followers_count: Optional[int]
    profile_picture_url: Optional[str]
    
class Influencer(InfluencerBase, table=True):
    """
    Database model for an influencer.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # AI-generated fields
    main_category: Optional[InfluencerCategory]
    strengths: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))
    weaknesses: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))
    predominant_style: Optional[str]

    posts: List["Post"] = Relationship(back_populates="influencer")

class InfluencerRead(InfluencerBase):
    """
    Read model for an influencer.
    """
    id: int

class InfluencerReadWithPosts(InfluencerRead):
    """
    Read model for an influencer with their posts.
    """
    posts: List[Post] = [] 
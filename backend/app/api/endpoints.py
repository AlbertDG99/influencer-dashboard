from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, SQLModel, select

from app.db.session import get_session
from app.models.influencer import Influencer, InfluencerRead, InfluencerReadWithPosts
from app.models.instagram import InstagramProfile
from app.tasks.analysis import analyze_influencer_profile
from app.services import instagram_service

router = APIRouter()

@router.get("/ping")
def ping():
    """Simple health check endpoint."""
    return {"status": "ok"}

@router.get("/instagram/profile/{username}", response_model=InstagramProfile)
def get_instagram_profile(username: str):
    """
    Obtiene la información del perfil de un usuario de Instagram.
    """
    profile = instagram_service.get_profile_info(username)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found or error fetching data.")
    return profile

@router.get("/instagram/discover/{hashtag}", response_model=List[InstagramProfile])
def discover_influencers_by_hashtag(hashtag: str):
    """
    Descubre influencers con más de 50k seguidores a partir de un hashtag.
    Este proceso puede tardar varios minutos.
    """
    influencers = instagram_service.discover_influencers(hashtag)
    if not influencers:
        raise HTTPException(status_code=404, detail="No influencers found for this hashtag or an error occurred.")
    return influencers

class InfluencerCreate(SQLModel):
    username: str

@router.post("/influencers", response_model=InfluencerRead)
def create_influencer(influencer: InfluencerCreate, session: Session = Depends(get_session)):
    """
    Add a new influencer to the database and trigger analysis.
    """
    db_influencer = session.exec(select(Influencer).where(Influencer.username == influencer.username)).first()
    if db_influencer:
        raise HTTPException(status_code=400, detail="Influencer with this username already exists.")
    
    new_influencer = Influencer(username=influencer.username)
    session.add(new_influencer)
    session.commit()
    session.refresh(new_influencer)
    
    # Trigger background task for analysis
    analyze_influencer_profile.delay(new_influencer.id)
    
    return new_influencer

@router.get("/influencers", response_model=List[InfluencerRead])
def read_influencers(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    """
    Get a list of all influencers.
    """
    influencers = session.exec(select(Influencer).offset(skip).limit(limit)).all()
    return influencers

@router.get("/influencers/{influencer_id}", response_model=InfluencerReadWithPosts)
def read_influencer(influencer_id: int, session: Session = Depends(get_session)):
    """
    Get a single influencer by ID.
    """
    influencer = session.get(Influencer, influencer_id)
    if not influencer:
        raise HTTPException(status_code=404, detail="Influencer not found")
    return influencer 
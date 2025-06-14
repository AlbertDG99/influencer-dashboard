from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.influencer import Influencer, InfluencerRead, InfluencerReadWithPosts
from app.tasks.analysis import analyze_influencer_profile
from app.services.instagram_scraper import get_public_user_info as get_instagram_profile_data

router = APIRouter()

@router.get("/instagram-profile/{username}")
async def get_instagram_profile(username: str):
    """
    Endpoint to get public information from an Instagram profile.
    NOTE: This uses an unofficial scraping method and may break without notice.
    """
    print(f"--- Backend: Recibida petición para el usuario: {username} ---")
    profile_data = get_instagram_profile_data(username)
    
    if not profile_data:
        print(f"--- Backend: No se encontraron datos para {username}. Devolviendo 404. ---")
        raise HTTPException(
            status_code=404,
            detail="Instagram profile not found or is private."
        )
        
    print(f"--- Backend: Datos encontrados para {username}. Devolviendo 200 OK. ---")
    return profile_data

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
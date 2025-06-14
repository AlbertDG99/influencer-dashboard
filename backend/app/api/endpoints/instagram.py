from fastapi import APIRouter, HTTPException
from app.services.instagram_scraper import get_public_user_info

router = APIRouter()

@router.get("/profile/{username}")
async def get_instagram_profile(username: str):
    """
    Endpoint para obtener la información pública de un perfil de Instagram.
    """
    profile_data = get_public_user_info(username)
    
    if not profile_data:
        raise HTTPException(
            status_code=404,
            detail="Perfil de Instagram no encontrado o es privado."
        )
        
    return profile_data 
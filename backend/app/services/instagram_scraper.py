import instaloader
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def get_public_user_info(username: str):
    """
    Obtiene información pública de un perfil de Instagram utilizando la librería Instaloader.
    """
    log.info(f"Attempting to fetch public info for username: {username}")
    
    L = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=True,
    )

    try:
        # Obtenemos el objeto Profile
        profile = instaloader.Profile.from_username(L.context, username)
        log.info(f"Successfully fetched profile for {username}")

        # Extraemos la información relevante
        latest_post = next(profile.get_posts(), None)
        latest_post_url = latest_post.url if latest_post else None
        
        profile_info = {
            'username': profile.username,
            'full_name': profile.full_name,
            'biography': profile.biography,
            'followers_count': profile.followers,
            'following_count': profile.followees,
            'profile_pic_url': profile.profile_pic_url,
            'is_private': profile.is_private,
            'is_verified': profile.is_verified,
            'media_count': profile.mediacount,
            'latest_post_url': latest_post_url,
        }
        
        return profile_info

    except instaloader.exceptions.ProfileNotFound:
        # El perfil no existe
        log.warning(f"Profile not found for username: {username}")
        return None
    except Exception as e:
        # Otro tipo de error (ej: conexión, rate limit)
        # En un entorno de producción, sería bueno loggear este error 'e'
        log.error(f"An unexpected error occurred while fetching profile for {username}: {e}", exc_info=True)
        return None 

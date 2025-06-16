import httpx
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

# Cliente HTTP con cabeceras para simular una petición de la web de Instagram
# La cabecera x-ig-app-id es fundamental.
client = httpx.Client(
    headers={
        "x-ig-app-id": "936619743392459",  # ID de la app web de Instagram
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
)

def get_public_user_info(username: str):
    """
    Obtiene información pública de un perfil de Instagram utilizando un endpoint
    de la API interna de la web.
    Técnica basada en: https://scrapfly.io/blog/how-to-scrape-instagram/
    """
    url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
    log.info(f"Attempting to fetch profile from API: {url}")
    
    try:
        response = client.get(url, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        user_data = data.get('data', {}).get('user')

        if not user_data:
            log.error(f"Could not find user data in the API response for username: {username}")
            return None

        # Extraemos la información relevante
        latest_post_edge = user_data.get('edge_owner_to_timeline_media', {}).get('edges', [])
        latest_post_url = None
        if latest_post_edge:
            latest_post_url = latest_post_edge[0].get('node', {}).get('display_url')

        profile_info = {
            'username': user_data.get('username'),
            'full_name': user_data.get('full_name'),
            'biography': user_data.get('biography'),
            'followers_count': user_data.get('edge_followed_by', {}).get('count'),
            'following_count': user_data.get('edge_follow', {}).get('count'),
            'profile_pic_url': user_data.get('profile_pic_url_hd'),
            'is_private': user_data.get('is_private'),
            'is_verified': user_data.get('is_verified'),
            'media_count': user_data.get('edge_owner_to_timeline_media', {}).get('count'),
            'latest_post_url': latest_post_url,
        }
        
        log.info(f"Successfully fetched data for {username} from API")
        return profile_info

    except httpx.HTTPStatusError as http_err:
        log.error(f"HTTP error occurred for {username}: {http_err} - Status code: {http_err.response.status_code}")
        log.error(f"Response body: {http_err.response.text}")
        return None
    except Exception as e:
        log.error(f"An unexpected error occurred while fetching {username}: {e}", exc_info=True)
        return None 

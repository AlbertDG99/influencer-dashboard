from . import instagram_scraper
from ..models.instagram import InstagramProfile
import time
import random

def get_mock_instagram_data(username: str):
    """
    Returns mock data simulating a call to the Instagram API.
    In a real application, this function would use the Instagram Graph API.
    """
    print(f"--- MOCK INSTAGRAM API: Fetching data for {username} ---")

    # Mock profile data
    mock_profile = {
        "username": username,
        "full_name": f"{username.replace('_', ' ').title()}",
        "biography": f"Bio for {username} | Just a mock profile 🚀",
        "followers_count": 12345,
        "profile_pic_url": f"https://source.unsplash.com/200x200/?portrait,{username}",
    }

    # Mock posts data
    mock_posts = [
        {
            "id": f"mock_post_1_{username}",
            "display_url": "https://source.unsplash.com/800x800/?fashion",
            "caption": "Loving this new outfit! #fashion #style",
            "likes_count": 1500,
            "comments_count": 50
        },
        {
            "id": f"mock_post_2_{username}",
            "display_url": "https://source.unsplash.com/800x800/?travel",
            "caption": "Adventures in the mountains. #travel #adventure",
            "likes_count": 2200,
            "comments_count": 80
        },
        {
            "id": f"mock_post_3_{username}",
            "display_url": "https://source.unsplash.com/800x800/?food",
            "caption": "Best pasta I've ever had. #foodie #food",
            "likes_count": 1800,
            "comments_count": 120
        },
    ]
    
    print(f"--- MOCK INSTAGRAM API: Found profile and {len(mock_posts)} posts ---")

    return mock_profile, mock_posts 

def get_profile_info(username: str) -> InstagramProfile:
    """Obtiene y procesa la información de un perfil."""
    profile_data = instagram_scraper.get_public_user_info(username)
    if profile_data:
        return InstagramProfile(**profile_data)
    return None

def discover_influencers(hashtag: str, min_followers: int = 50000, limit: int = 10):
    """
    Descubre hasta `limit` influencers con más de `min_followers` seguidores
    a partir de un hashtag.
    """
    usernames = instagram_scraper.scrape_users_by_hashtag(hashtag)
    influencers = []
    
    for username in usernames:
        # Si ya hemos encontrado suficientes, paramos.
        if len(influencers) >= limit:
            break
            
        # Pausa aleatoria para no saturar la API
        sleep_time = random.uniform(2, 5)
        time.sleep(sleep_time)
        
        profile_data = instagram_scraper.get_public_user_info(username)
        
        if profile_data and profile_data.get('followers_count', 0) > min_followers:
            influencers.append(InstagramProfile(**profile_data))
            
    return influencers 
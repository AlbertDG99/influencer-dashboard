import requests
import json

def get_public_user_info(username: str):
    """
    Obtiene información pública de un perfil de Instagram utilizando
    un endpoint no oficial.
    """
    url = f"https://www.instagram.com/{username}/?__a=1&__d=dis"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        user_data = data.get('graphql', {}).get('user', {})

        if not user_data:
            return None

        # Extraemos la información relevante, incluyendo la última publicación
        latest_post = user_data.get('edge_owner_to_timeline_media', {}).get('edges', [])
        latest_post_url = None
        if latest_post:
            latest_post_url = latest_post[0].get('node', {}).get('display_url')

        profile_info = {
            'username': user_data.get('username'),
            'full_name': user_data.get('full_name'),
            'biography': user_data.get('biography'),
            'followers_count': user_data.get('edge_followed_by', {}).get('count'),
            'following_count': user_data.get('edge_follow', {}).get('count'),
            'profile_pic_url': user_data.get('profile_pic_url_hd'),
            'latest_post_url': latest_post_url
        }
        
        return profile_info

    except requests.exceptions.HTTPError:
        # Podríamos loggear el error, pero para el cliente es suficiente con saber que no se encontró
        return None
    except Exception:
        # Igual aquí, loggear sería ideal en producción
        return None 

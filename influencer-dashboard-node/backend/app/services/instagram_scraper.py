import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

# Instagram session tokens - HARDCODED para desarrollo
INSTAGRAM_SESSIONID = "75504450607%3AGCAU8mkXVXcoA8%3A23%3AAYdhhDR59F_Lg9jLXDuDpt0w4s7jny9WtIy9kdTQiA"
INSTAGRAM_CSRFTOKEN = "xslYDVPlILcRY8w21xzsKCpNWOlwwaVz"
INSTAGRAM_DS_USER_ID = "75504450607"
INSTAGRAM_ALL_COOKIES = "csrftoken=xslYDVPlILcRY8w21xzsKCpNWOlwwaVz; mid=KcvMaaiJBXMdJ2f-MPg3; dpr=1304347826086565; sessionid=75504450607%3AGCAU8mkXVXcoA8%3A23%3AAYdhhDR59F_Lg9jLXDuDpt0w4s7jny9WtIy9kdTQiA; ds_user_id=75504450607; ig_did=3E5F5B81-624F-42EE-9332-E3C0E5D8B376; rur=AshRAGAahlhAaZXzFmSFnGAIpX; shbid=6EINV0S47G6o6VDa47hYzGXXWWXlHfCa37a8bc3800ab87d4d5c5bf4dSfPSfRbKG6QWlnGlA; shbts=1735043991"

def set_instagram_auth(sessionid: str, csrftoken: str, ds_user_id: str):
    """Set Instagram authentication tokens"""
    global INSTAGRAM_SESSIONID, INSTAGRAM_CSRFTOKEN, INSTAGRAM_DS_USER_ID
    INSTAGRAM_SESSIONID = sessionid
    INSTAGRAM_CSRFTOKEN = csrftoken
    INSTAGRAM_DS_USER_ID = ds_user_id
    log.info("🔐 Instagram authentication tokens set successfully")

def set_instagram_full_auth(all_cookies_string: str):
    """
    Set complete Instagram authentication using all browser cookies.
    This provides better authentication than just the 3 basic tokens.
    
    Args:
        all_cookies_string: Complete cookie string from browser (e.g., "sessionid=...; csrftoken=...; ds_user_id=...; ig_did=...; etc")
    """
    global INSTAGRAM_ALL_COOKIES, INSTAGRAM_SESSIONID, INSTAGRAM_CSRFTOKEN, INSTAGRAM_DS_USER_ID
    
    INSTAGRAM_ALL_COOKIES = all_cookies_string
    
    # Extraer tokens individuales para compatibilidad
    cookies_dict = {}
    for cookie in all_cookies_string.split(';'):
        if '=' in cookie:
            key, value = cookie.strip().split('=', 1)
            cookies_dict[key.strip()] = value.strip()
    
    INSTAGRAM_SESSIONID = cookies_dict.get('sessionid', '')
    INSTAGRAM_CSRFTOKEN = cookies_dict.get('csrftoken', '')
    INSTAGRAM_DS_USER_ID = cookies_dict.get('ds_user_id', '')
    
    log.info(f"🔐 Instagram FULL authentication set with {len(cookies_dict)} cookies")
    log.info(f"   Available cookies: {list(cookies_dict.keys())}")

def get_authenticated_headers():
    """Get headers with authentication cookies"""
    if INSTAGRAM_ALL_COOKIES:
        # Usar todas las cookies para mejor autenticación
        import urllib.parse
        
        # Decodificar sessionid si está en las cookies
        cookie_string = INSTAGRAM_ALL_COOKIES
        if 'sessionid=' in cookie_string and '%3A' in cookie_string:
            # Buscar y decodificar sessionid
            parts = cookie_string.split(';')
            for i, part in enumerate(parts):
                if 'sessionid=' in part:
                    key, value = part.strip().split('=', 1)
                    decoded_value = urllib.parse.unquote(value)
                    parts[i] = f"{key}={decoded_value}"
            cookie_string = '; '.join(parts)
        
        return {
            'Cookie': cookie_string,
            'X-CSRFToken': INSTAGRAM_CSRFTOKEN,
            'X-IG-App-ID': '936619743392459',  # CRÍTICO
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.instagram.com/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }
    elif all([INSTAGRAM_SESSIONID, INSTAGRAM_CSRFTOKEN, INSTAGRAM_DS_USER_ID]):
        # Fallback a método anterior
        import urllib.parse
        sessionid = urllib.parse.unquote(INSTAGRAM_SESSIONID)
        
        return {
            'Cookie': f'sessionid={sessionid}; csrftoken={INSTAGRAM_CSRFTOKEN}; ds_user_id={INSTAGRAM_DS_USER_ID}',
            'X-CSRFToken': INSTAGRAM_CSRFTOKEN,
            'X-IG-App-ID': '936619743392459',
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.instagram.com/',
        }
    else:
        return {}

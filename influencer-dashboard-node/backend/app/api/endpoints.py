from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import json
import asyncio

from app.services.instagram_scraper import (
    set_instagram_auth,
    set_instagram_full_auth
)
from app.services.instagram_selenium_scraper import scrape_with_selenium

router = APIRouter()

@router.get("/ping")
def ping():
    """Simple health check endpoint."""
    return {"status": "ok", "message": "Instagram Selenium Scraper API is running"}

@router.post("/instagram/auth")
def set_instagram_authentication(sessionid: str, csrftoken: str, ds_user_id: str):
    """
    Configura los tokens de autenticación de Instagram para acceso completo.
    Permite obtener TODOS los posts sin limitaciones de 12 posts.
    """
    try:
        set_instagram_auth(sessionid, csrftoken, ds_user_id)
        return {
            "status": "success", 
            "message": "🔐 Instagram authentication configured successfully! Now you can access ALL posts without limitations."
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error setting authentication: {str(e)}")

@router.post("/instagram/auth/full")
def set_instagram_full_authentication(cookies: str):
    """
    Configura autenticación completa de Instagram usando todas las cookies del navegador.
    Esto proporciona mejor autenticación que solo los 3 tokens básicos.
    
    Args:
        cookies: String completo de cookies del navegador (ej: "sessionid=...; csrftoken=...; ds_user_id=...; ig_did=...; etc")
    """
    try:
        set_instagram_full_auth(cookies)
        return {
            "status": "success", 
            "message": "🔐 Instagram FULL authentication configured successfully! Using complete browser session for maximum access."
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error setting full authentication: {str(e)}")

@router.get("/instagram/auth/status")
def get_authentication_status():
    """
    Verifica el estado de la autenticación de Instagram.
    """
    from app.services.instagram_scraper import INSTAGRAM_SESSIONID, INSTAGRAM_CSRFTOKEN, INSTAGRAM_DS_USER_ID, INSTAGRAM_ALL_COOKIES
    
    is_full_authenticated = bool(INSTAGRAM_ALL_COOKIES)
    is_basic_authenticated = all([INSTAGRAM_SESSIONID, INSTAGRAM_CSRFTOKEN, INSTAGRAM_DS_USER_ID])
    
    if is_full_authenticated:
        # Contar cookies disponibles
        cookie_count = len([c for c in INSTAGRAM_ALL_COOKIES.split(';') if '=' in c])
        
        return {
            "status": "full_authenticated",
            "message": "🔐 Instagram FULL authentication is active",
            "user_id": INSTAGRAM_DS_USER_ID,
            "cookie_count": cookie_count,
            "auth_type": "Complete browser session",
            "benefits": [
                "Maximum authentication level",
                "All browser cookies included",
                "Best chance to access all posts",
                "Reduced rate limiting",
                "Access to private content (if authorized)",
                "Complete video content access"
            ]
        }
    elif is_basic_authenticated:
        return {
            "status": "basic_authenticated",
            "message": "🔐 Instagram basic authentication is active",
            "user_id": INSTAGRAM_DS_USER_ID,
            "auth_type": "Basic tokens only",
            "benefits": [
                "Access to complete user profiles",
                "Potential access to more posts than public limit",
                "Better rate limiting tolerance",
                "Access to private content (if authorized)"
            ]
        }
    else:
        return {
            "status": "not_authenticated", 
            "message": "❌ No Instagram authentication configured",
            "auth_type": "Public only",
            "limitations": [
                "Limited to ~12 posts per profile",
                "Cannot access private profiles",
                "Subject to strict rate limiting",
                "No access to complete video content"
            ]
        }

@router.post("/instagram/scrape-selenium/{username}")
async def scrape_instagram_with_selenium(username: str, cookies: str = None):
    """
    🔥 SCRAPING MANUAL CON SELENIUM - ENGAÑAR A INSTAGRAM
    
    Usa Selenium para simular un navegador real y engañar las medidas anti-scraping de Instagram.
    Este método:
    - Simula comportamiento humano (delays, scroll, clics)
    - Usa tu sesión completa de navegador con todas las cookies
    - Hace scroll manual para cargar TODOS los posts
    - Extrae datos directamente del DOM como un humano
    - Evita las limitaciones de las APIs de Instagram
    
    Args:
        username: Nombre de usuario de Instagram (sin @)
        cookies: String completo de cookies de tu navegador
    
    Returns:
        Información completa del perfil y TODOS los posts disponibles
    """
    try:
        # Ejecutar scraping con Selenium
        result = await scrape_with_selenium(username, cookies)
        
        if not result.get('success'):
            raise HTTPException(
                status_code=400, 
                detail=f"Error en scraping con Selenium: {result.get('error', 'Unknown error')}"
            )
        
        # Preparar respuesta con información detallada
        response = {
            "success": True,
            "method": "selenium_manual_scraping",
            "username": username,
            "profile": result.get('profile', {}),
            "posts": result.get('posts', []),
            "statistics": {
                "total_posts_in_profile": result.get('profile', {}).get('posts_count', 0),
                "posts_scraped": result.get('total_posts_found', 0),
                "posts_loaded_by_scroll": result.get('posts_loaded_by_scroll', 0),
                "scraping_effectiveness": f"{result.get('total_posts_found', 0)}/{result.get('profile', {}).get('posts_count', 0)} posts"
            },
            "selenium_info": {
                "browser_used": "Chrome with human simulation",
                "authentication_status": result.get('authenticated', False),
                "anti_detection_measures": [
                    "Human-like delays (2-5 seconds)",
                    "Random scroll patterns",
                    "Realistic user agent",
                    "Complete browser session simulation",
                    "DOM manipulation detection avoidance"
                ]
            },
            "message": f"🎉 Selenium scraping completado: {result.get('total_posts_found', 0)} posts extraídos de @{username}"
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno en scraping con Selenium: {str(e)}"
        )

@router.get("/instagram/scrape-selenium-stream/{username}")
async def scrape_instagram_selenium_stream(username: str, cookies: str = None):
    """
    🔥 SCRAPING MANUAL CON SELENIUM - VERSIÓN STREAMING
    
    Versión streaming del scraping con Selenium que muestra progreso en tiempo real.
    Permite ver el proceso de scraping mientras ocurre.
    """
    async def generate_selenium_progress():
        try:
            start_msg = f"🚀 Iniciando scraping manual con Selenium para @{username}"
            yield f"data: {json.dumps({'type': 'start', 'message': start_msg})}\n\n"
            yield f"data: {json.dumps({'type': 'info', 'message': '🔧 Configurando navegador Chrome con medidas anti-detección...'})}\n\n"
            
            # Ejecutar scraping
            result = await scrape_with_selenium(username, cookies)
            
            if result.get('success'):
                yield f"data: {json.dumps({'type': 'success', 'message': '✅ Scraping completado exitosamente'})}\n\n"
                yield f"data: {json.dumps({'type': 'profile', 'data': result.get('profile', {})})}\n\n"
                yield f"data: {json.dumps({'type': 'posts', 'data': result.get('posts', [])})}\n\n"
                
                stats_data = {
                    'total_posts': result.get('total_posts_found', 0), 
                    'profile_posts': result.get('profile', {}).get('posts_count', 0)
                }
                yield f"data: {json.dumps({'type': 'statistics', 'data': stats_data})}\n\n"
                
                total_posts = result.get("total_posts_found", 0)
                complete_msg = f"🎉 {total_posts} posts extraídos exitosamente"
                yield f"data: {json.dumps({'type': 'complete', 'message': complete_msg})}\n\n"
            else:
                error_msg = result.get("error", "Unknown error")
                yield f"data: {json.dumps({'type': 'error', 'message': f'❌ Error: {error_msg}'})}\n\n"
                
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': f'❌ Error interno: {str(e)}'})}\n\n"
    
    return StreamingResponse(
        generate_selenium_progress(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Cache-Control"
        }
    ) 
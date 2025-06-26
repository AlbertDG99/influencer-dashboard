#!/usr/bin/env python3
"""
Test script para el scraper de Instagram con Selenium
"""

import asyncio
import json
import sys
import os

# Añadir el directorio backend al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.instagram_selenium_scraper import scrape_with_selenium

async def test_selenium_scraper():
    """
    Prueba el scraper de Selenium con el perfil de albertodfg99
    """
    print("🔥 INICIANDO TEST DEL SCRAPER CON SELENIUM")
    print("=" * 60)
    
    # Configuración del test
    username = "albertodfg99"
    cookies = "csrftoken=xslYDVPlILcRY8w21xzsKCpNWOlwwaVz; mid=KcvMaaiJBXMdJ2f-MPg3; dpr=1304347826086565; sessionid=75504450607%3AGCAU8mkXVXcoA8%3A23%3AAYdhhDR59F_Lg9jLXDuDpt0w4s7jny9WtIy9kdTQiA; ds_user_id=75504450607; ig_did=3E5F5B81-624F-42EE-9332-E3C0E5D8B376; rur=AshRAGAahlhAaZXzFmSFnGAIpX; shbid=6EINV0S47G6o6VDa47hYzGXXWWXlHfCa37a8bc3800ab87d4d5c5bf4dSfPSfRbKG6QWlnGlA; shbts=1735043991"
    
    print(f"👤 Perfil objetivo: @{username}")
    print(f"🍪 Cookies configuradas: {len(cookies.split(';'))} cookies")
    print()
    
    try:
        # Ejecutar scraping
        print("🚀 Ejecutando scraping con Selenium...")
        result = await scrape_with_selenium(username, cookies)
        
        print("📊 RESULTADOS DEL SCRAPING:")
        print("=" * 40)
        
        if result.get('success'):
            print("✅ SCRAPING EXITOSO!")
            print()
            
            # Información del perfil
            profile = result.get('profile', {})
            print("👤 INFORMACIÓN DEL PERFIL:")
            print(f"   Username: {profile.get('username', 'N/A')}")
            print(f"   Nombre completo: {profile.get('full_name', 'N/A')}")
            print(f"   Posts: {profile.get('posts_count', 0)}")
            print(f"   Followers: {profile.get('followers_count', 0)}")
            print(f"   Following: {profile.get('following_count', 0)}")
            print(f"   Privado: {'Sí' if profile.get('is_private', False) else 'No'}")
            print(f"   Verificado: {'Sí' if profile.get('is_verified', False) else 'No'}")
            print()
            
            # Estadísticas de scraping
            posts_data = result.get('posts', [])
            total_posts_found = len(posts_data)
            posts_in_profile = profile.get('posts_count', 0)
            
            print("📈 ESTADÍSTICAS DE SCRAPING:")
            print(f"   Posts en el perfil: {posts_in_profile}")
            print(f"   Posts encontrados: {total_posts_found}")
            print(f"   Efectividad: {total_posts_found}/{posts_in_profile} ({(total_posts_found/posts_in_profile*100) if posts_in_profile > 0 else 0:.1f}%)")
            print(f"   Método: {result.get('scraping_method', 'N/A')}")
            print(f"   Autenticado: {'Sí' if result.get('authenticated', False) else 'No'}")
            print()
            
            # Mostrar algunos posts
            if posts_data:
                print("📸 PRIMEROS POSTS ENCONTRADOS:")
                for i, post in enumerate(posts_data[:5]):
                    print(f"   Post {i+1}:")
                    print(f"     Shortcode: {post.get('shortcode', 'N/A')}")
                    print(f"     Tipo: {post.get('type', 'N/A')}")
                    print(f"     URL: {post.get('url', 'N/A')[:50]}...")
                    print()
                
                if len(posts_data) > 5:
                    print(f"   ... y {len(posts_data) - 5} posts más")
                    print()
            
            # Comparación con métodos anteriores
            print("🔍 COMPARACIÓN CON MÉTODOS ANTERIORES:")
            print(f"   Método público: ~12 posts")
            print(f"   Método autenticado: ~12 posts")
            print(f"   Selenium manual: {total_posts_found} posts")
            print()
            
            if total_posts_found > 12:
                print("🎉 ¡ÉXITO! Selenium ha superado las limitaciones de Instagram")
                print(f"   Se obtuvieron {total_posts_found - 12} posts adicionales")
            elif total_posts_found == posts_in_profile:
                print("🎉 ¡PERFECTO! Se obtuvieron TODOS los posts del perfil")
            else:
                print("⚠️ Selenium obtuvo los mismos resultados que métodos anteriores")
                print("   Instagram mantiene sus limitaciones incluso con navegador real")
            
        else:
            print("❌ SCRAPING FALLÓ")
            print(f"   Error: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ ERROR DURANTE EL TEST: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 60)
    print("🏁 TEST COMPLETADO")

if __name__ == "__main__":
    # Ejecutar test
    asyncio.run(test_selenium_scraper()) 
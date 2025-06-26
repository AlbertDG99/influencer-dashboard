#!/usr/bin/env python3
"""
Test script para probar el nuevo endpoint de Selenium via API
"""

import requests
import json
import time

def test_selenium_api():
    """
    Prueba el endpoint de Selenium scraping via API
    """
    print("🔥 PROBANDO ENDPOINT DE SELENIUM VIA API")
    print("=" * 60)
    
    # Configuración
    base_url = "http://localhost:8000/api/v1"
    username = "albertodfg99"
    cookies = "csrftoken=xslYDVPlILcRY8w21xzsKCpNWOlwwaVz; mid=KcvMaaiJBXMdJ2f-MPg3; dpr=1304347826086565; sessionid=75504450607%3AGCAU8mkXVXcoA8%3A23%3AAYdhhDR59F_Lg9jLXDuDpt0w4s7jny9WtIy9kdTQiA; ds_user_id=75504450607; ig_did=3E5F5B81-624F-42EE-9332-E3C0E5D8B376; rur=AshRAGAahlhAaZXzFmSFnGAIpX; shbid=6EINV0S47G6o6VDa47hYzGXXWWXlHfCa37a8bc3800ab87d4d5c5bf4dSfPSfRbKG6QWlnGlA; shbts=1735043991"
    
    print(f"🌐 URL Base: {base_url}")
    print(f"👤 Usuario: @{username}")
    print(f"🍪 Cookies: {len(cookies.split(';'))} cookies configuradas")
    print()
    
    # Primero verificar que el backend esté funcionando
    try:
        print("🔍 Verificando conexión con el backend...")
        response = requests.get(f"{base_url}/ping", timeout=10)
        if response.status_code == 200:
            print("✅ Backend conectado correctamente")
        else:
            print(f"❌ Error conectando al backend: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return
    
    print()
    
    # Probar el endpoint de Selenium
    try:
        print("🚀 Enviando solicitud de scraping con Selenium...")
        print("⏳ Esto puede tomar varios minutos...")
        
        # Preparar datos
        url = f"{base_url}/instagram/scrape-selenium/{username}"
        data = {"cookies": cookies}
        headers = {"Content-Type": "application/json"}
        
        # Enviar solicitud
        start_time = time.time()
        response = requests.post(url, json=data, timeout=300)  # 5 minutos timeout
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"⏱️ Tiempo transcurrido: {duration:.2f} segundos")
        print()
        
        if response.status_code == 200:
            print("✅ SOLICITUD EXITOSA!")
            
            # Parsear respuesta
            try:
                result = response.json()
                
                print("📊 RESULTADOS:")
                print("=" * 40)
                print(f"✅ Éxito: {result.get('success', False)}")
                print(f"🔧 Método: {result.get('method', 'N/A')}")
                print(f"👤 Usuario: {result.get('username', 'N/A')}")
                print()
                
                # Información del perfil
                profile = result.get('profile', {})
                if profile:
                    print("👤 PERFIL:")
                    print(f"   Nombre: {profile.get('full_name', 'N/A')}")
                    print(f"   Posts: {profile.get('posts_count', 0)}")
                    print(f"   Followers: {profile.get('followers_count', 0)}")
                    print(f"   Following: {profile.get('following_count', 0)}")
                    print()
                
                # Estadísticas
                stats = result.get('statistics', {})
                if stats:
                    print("📈 ESTADÍSTICAS:")
                    print(f"   Posts en perfil: {stats.get('total_posts_in_profile', 0)}")
                    print(f"   Posts scrapeados: {stats.get('posts_scraped', 0)}")
                    print(f"   Efectividad: {stats.get('scraping_effectiveness', 'N/A')}")
                    print()
                
                # Posts encontrados
                posts = result.get('posts', [])
                if posts:
                    print(f"📸 POSTS ENCONTRADOS: {len(posts)}")
                    for i, post in enumerate(posts[:3]):
                        print(f"   Post {i+1}: {post.get('shortcode', 'N/A')} ({post.get('type', 'N/A')})")
                    
                    if len(posts) > 3:
                        print(f"   ... y {len(posts) - 3} posts más")
                    print()
                
                # Información de Selenium
                selenium_info = result.get('selenium_info', {})
                if selenium_info:
                    print("🔧 INFORMACIÓN DE SELENIUM:")
                    print(f"   Navegador: {selenium_info.get('browser_used', 'N/A')}")
                    print(f"   Autenticado: {selenium_info.get('authentication_status', False)}")
                    print()
                
                # Mensaje final
                message = result.get('message', '')
                if message:
                    print(f"💬 MENSAJE: {message}")
                    print()
                
                # Análisis de resultados
                posts_scraped = stats.get('posts_scraped', 0)
                posts_in_profile = stats.get('total_posts_in_profile', 0)
                
                if posts_scraped > 12:
                    print("🎉 ¡ÉXITO! Selenium superó las limitaciones de Instagram")
                    print(f"   Se obtuvieron {posts_scraped - 12} posts adicionales")
                elif posts_scraped == posts_in_profile and posts_in_profile > 12:
                    print("🎉 ¡PERFECTO! Se obtuvieron TODOS los posts del perfil")
                else:
                    print("⚠️ Resultado similar a métodos anteriores")
                    print("   Instagram mantiene sus restricciones")
                
            except json.JSONDecodeError:
                print("❌ Error parseando respuesta JSON")
                print(f"Respuesta cruda: {response.text[:500]}...")
                
        else:
            print(f"❌ ERROR EN LA SOLICITUD: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Detalle del error: {error_data}")
            except:
                print(f"Respuesta de error: {response.text}")
    
    except requests.exceptions.Timeout:
        print("⏰ TIMEOUT: La solicitud tardó más de 5 minutos")
        print("   Esto puede ser normal para el scraping con Selenium")
    except Exception as e:
        print(f"❌ ERROR DURANTE LA SOLICITUD: {e}")
    
    print()
    print("=" * 60)
    print("🏁 PRUEBA COMPLETADA")

def test_selenium_stream_api():
    """
    Prueba el endpoint de streaming de Selenium
    """
    print()
    print("🔥 PROBANDO ENDPOINT DE SELENIUM STREAMING")
    print("=" * 60)
    
    base_url = "http://localhost:8000/api/v1"
    username = "albertodfg99"
    cookies = "csrftoken=xslYDVPlILcRY8w21xzsKCpNWOlwwaVz; mid=KcvMaaiJBXMdJ2f-MPg3; dpr=1304347826086565; sessionid=75504450607%3AGCAU8mkXVXcoA8%3A23%3AAYdhhDR59F_Lg9jLXDuDpt0w4s7jny9WtIy9kdTQiA; ds_user_id=75504450607; ig_did=3E5F5B81-624F-42EE-9332-E3C0E5D8B376; rur=AshRAGAahlhAaZXzFmSFnGAIpX; shbid=6EINV0S47G6o6VDa47hYzGXXWWXlHfCa37a8bc3800ab87d4d5c5bf4dSfPSfRbKG6QWlnGlA; shbts=1735043991"
    
    try:
        print("🚀 Conectando al stream de Selenium...")
        url = f"{base_url}/instagram/scrape-selenium-stream/{username}?cookies={cookies}"
        
        response = requests.get(url, stream=True, timeout=300)
        
        if response.status_code == 200:
            print("✅ Stream conectado, recibiendo datos...")
            print()
            
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        try:
                            data = json.loads(line_str[6:])  # Remover 'data: '
                            
                            msg_type = data.get('type', 'unknown')
                            message = data.get('message', '')
                            
                            if msg_type == 'start':
                                print(f"🚀 {message}")
                            elif msg_type == 'info':
                                print(f"ℹ️  {message}")
                            elif msg_type == 'success':
                                print(f"✅ {message}")
                            elif msg_type == 'error':
                                print(f"❌ {message}")
                            elif msg_type == 'complete':
                                print(f"🎉 {message}")
                            elif msg_type == 'profile':
                                profile = data.get('data', {})
                                print(f"👤 Perfil: {profile.get('posts_count', 0)} posts, {profile.get('followers_count', 0)} followers")
                            elif msg_type == 'posts':
                                posts = data.get('data', [])
                                print(f"📸 Posts extraídos: {len(posts)}")
                            elif msg_type == 'statistics':
                                stats = data.get('data', {})
                                print(f"📊 Stats: {stats.get('total_posts', 0)} posts encontrados")
                            else:
                                print(f"📡 {msg_type}: {message}")
                                
                        except json.JSONDecodeError:
                            print(f"📡 Raw: {line_str}")
        else:
            print(f"❌ Error en stream: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error en streaming: {e}")
    
    print()
    print("🏁 STREAM COMPLETADO")

if __name__ == "__main__":
    # Ejecutar pruebas
    test_selenium_api()
    
    # Opcional: también probar streaming
    # test_selenium_stream_api() 
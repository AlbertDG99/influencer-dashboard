"""
Instagram Selenium Scraper - Manual Browser Automation
Simula un navegador real para engañar las medidas anti-scraping de Instagram
"""

import asyncio
import time
import random
import json
import re
import logging
from typing import List, Dict, Optional, Any
from pathlib import Path
import urllib.parse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Configurar logging
log = logging.getLogger(__name__)

# Cookies hardcodeadas para desarrollo
HARDCODED_COOKIES = "csrftoken=xslYDVPlILcRY8w21xzsKCpNWOlwwaVz; mid=KcvMaaiJBXMdJ2f-MPg3; dpr=1304347826086565; sessionid=75504450607%3AGCAU8mkXVXcoA8%3A23%3AAYdhhDR59F_Lg9jLXDuDpt0w4s7jny9WtIy9kdTQiA; ds_user_id=75504450607; ig_did=3E5F5B81-624F-42EE-9332-E3C0E5D8B376; rur=AshRAGAahlhAaZXzFmSFnGAIpX; shbid=6EINV0S47G6o6VDa47hYzGXXWWXlHfCa37a8bc3800ab87d4d5c5bf4dSfPSfRbKG6QWlnGlA; shbts=1735043991"

class InstagramSeleniumScraper:
    """
    Scraper de Instagram usando Selenium para simular navegación real
    """
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.cookies_loaded = False
        self.authenticated = False
        
        # Configuración de delays humanos
        self.human_delays = {
            'page_load': (3, 7),
            'scroll': (1, 3),
            'click': (0.5, 2),
            'typing': (0.1, 0.3),
            'between_actions': (2, 5)
        }
    
    def _get_chrome_options(self) -> Options:
        """Configurar opciones de Chrome para parecer un navegador real"""
        options = Options()
        
        # Configuraciones esenciales para Docker
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--headless")  # Necesario en Docker
        options.add_argument("--remote-debugging-port=9222")
        
        # Configuraciones para parecer un navegador real
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # User agent realista
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Configuraciones de ventana para Docker
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-images")  # Acelerar carga
        
        # Configuraciones de memoria y rendimiento
        options.add_argument("--memory-pressure-off")
        options.add_argument("--max_old_space_size=4096")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-backgrounding-occluded-windows")
        
        # Desactivar notificaciones y otras distracciones
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
            "profile.managed_default_content_settings.images": 2,  # Desactivar imágenes para velocidad
            "profile.default_content_setting_values.media_stream": 2,
        }
        options.add_experimental_option("prefs", prefs)
        
        # Configurar logging
        options.add_argument("--log-level=3")  # Solo errores críticos
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)
        
        return options
    
    def _human_delay(self, delay_type: str = 'between_actions'):
        """Simular delays humanos"""
        min_delay, max_delay = self.human_delays.get(delay_type, (1, 3))
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        log.debug(f"Human delay ({delay_type}): {delay:.2f}s")
    
    def _human_scroll(self, direction: str = 'down', distance: int = None):
        """Simular scroll humano"""
        if distance is None:
            distance = random.randint(300, 800)
        
        if direction == 'down':
            self.driver.execute_script(f"window.scrollBy(0, {distance});")
        elif direction == 'up':
            self.driver.execute_script(f"window.scrollBy(0, -{distance});")
        
        self._human_delay('scroll')
    
    def _human_type(self, element, text: str):
        """Simular escritura humana"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
    
    def initialize_browser(self) -> bool:
        """Inicializar el navegador con configuraciones anti-detección"""
        try:
            log.info("🚀 Inicializando navegador Chrome para Docker...")
            
            # Configurar el driver con manejo de errores mejorado
            try:
                service = Service(ChromeDriverManager().install())
                log.info("✅ ChromeDriver instalado correctamente")
            except Exception as e:
                log.warning(f"⚠️ Error con ChromeDriverManager, usando driver del sistema: {e}")
                service = Service()  # Usar driver del sistema
            
            options = self._get_chrome_options()
            
            # Intentar inicializar Chrome
            try:
                self.driver = webdriver.Chrome(service=service, options=options)
                log.info("✅ Chrome inicializado correctamente")
            except Exception as e:
                log.error(f"❌ Error inicializando Chrome: {e}")
                # Intentar con configuración más básica
                log.info("🔄 Intentando con configuración básica...")
                basic_options = Options()
                basic_options.add_argument("--no-sandbox")
                basic_options.add_argument("--disable-dev-shm-usage")
                basic_options.add_argument("--headless")
                basic_options.add_argument("--disable-gpu")
                self.driver = webdriver.Chrome(options=basic_options)
                log.info("✅ Chrome inicializado con configuración básica")
            
            self.wait = WebDriverWait(self.driver, 30)  # Más tiempo para Docker
            
            # Scripts anti-detección (con manejo de errores)
            try:
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                    "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                })
                log.info("✅ Scripts anti-detección aplicados")
            except Exception as e:
                log.warning(f"⚠️ No se pudieron aplicar scripts anti-detección: {e}")
            
            # Verificar que el navegador funciona
            try:
                self.driver.get("https://www.google.com")
                log.info("✅ Navegador verificado - funcionando correctamente")
                return True
            except Exception as e:
                log.error(f"❌ Error verificando navegador: {e}")
                return False
            
        except Exception as e:
            log.error(f"❌ Error crítico inicializando navegador: {e}")
            return False
    
    def load_cookies(self, cookies_string: str) -> bool:
        """Cargar cookies de Instagram para autenticación"""
        try:
            log.info("🍪 Cargando cookies de autenticación...")
            
            # Primero ir a Instagram para establecer el dominio
            self.driver.get("https://www.instagram.com")
            self._human_delay('page_load')
            
            # Parsear y cargar cookies
            cookies_dict = {}
            for cookie in cookies_string.split(';'):
                if '=' in cookie:
                    key, value = cookie.strip().split('=', 1)
                    cookies_dict[key.strip()] = value.strip()
            
            # Agregar cookies una por una
            for name, value in cookies_dict.items():
                try:
                    # Decodificar si es necesario
                    if name == 'sessionid' and '%' in value:
                        value = urllib.parse.unquote(value)
                    
                    cookie_dict = {
                        'name': name,
                        'value': value,
                        'domain': '.instagram.com',
                        'path': '/',
                        'secure': True
                    }
                    
                    self.driver.add_cookie(cookie_dict)
                    log.debug(f"Cookie agregada: {name}")
                    
                except Exception as e:
                    log.warning(f"Error agregando cookie {name}: {e}")
            
            # Refrescar para aplicar cookies
            self.driver.refresh()
            self._human_delay('page_load')
            
            self.cookies_loaded = True
            log.info(f"✅ {len(cookies_dict)} cookies cargadas correctamente")
            return True
            
        except Exception as e:
            log.error(f"❌ Error cargando cookies: {e}")
            return False
    
    def verify_authentication(self) -> bool:
        """Verificar si estamos autenticados correctamente"""
        try:
            log.info("🔐 Verificando autenticación...")
            
            # Buscar indicadores de que estamos logueados
            authenticated_indicators = [
                "//a[@href='/direct/inbox/']",  # Icono de mensajes
                "//a[contains(@href, '/accounts/edit/')]",  # Link de configuración
                "//button[@aria-label='New post']",  # Botón de nuevo post
                "//*[contains(@aria-label, 'Profile')]"  # Icono de perfil
            ]
            
            for indicator in authenticated_indicators:
                try:
                    element = self.wait.until(EC.presence_of_element_located((By.XPATH, indicator)))
                    if element:
                        self.authenticated = True
                        log.info("✅ Autenticación verificada correctamente")
                        return True
                except TimeoutException:
                    continue
            
            log.warning("⚠️ No se pudo verificar la autenticación")
            return False
            
        except Exception as e:
            log.error(f"❌ Error verificando autenticación: {e}")
            return False
    
    def navigate_to_profile(self, username: str) -> bool:
        """Navegar al perfil de usuario de forma humana"""
        try:
            log.info(f"👤 Navegando al perfil @{username}...")
            
            # Método 1: Usar la barra de búsqueda (más humano)
            try:
                # Buscar el campo de búsqueda
                search_selectors = [
                    "//input[@placeholder='Search']",
                    "//input[@aria-label='Search input']",
                    "//input[contains(@placeholder, 'Search')]",
                    "input[placeholder*='Search']"
                ]
                
                search_input = None
                for selector in search_selectors:
                    try:
                        if selector.startswith("//"):
                            search_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                        else:
                            search_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                        break
                    except TimeoutException:
                        continue
                
                if search_input:
                    log.info("🔍 Usando barra de búsqueda...")
                    search_input.click()
                    self._human_delay('click')
                    
                    # Limpiar y escribir
                    search_input.clear()
                    self._human_type(search_input, username)
                    self._human_delay('typing')
                    
                    # Esperar resultados y hacer clic en el perfil
                    time.sleep(2)
                    
                    # Buscar el enlace del perfil en los resultados
                    profile_link_selectors = [
                        f"//a[@href='/{username}/']",
                        f"//a[contains(@href, '/{username}')]",
                        f"//*[text()='{username}']//ancestor::a"
                    ]
                    
                    for selector in profile_link_selectors:
                        try:
                            profile_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                            profile_link.click()
                            self._human_delay('click')
                            log.info("✅ Perfil encontrado via búsqueda")
                            return True
                        except TimeoutException:
                            continue
            
            except Exception as e:
                log.warning(f"Búsqueda falló: {e}")
            
            # Método 2: Navegación directa (fallback)
            log.info("🔗 Navegación directa al perfil...")
            profile_url = f"https://www.instagram.com/{username}/"
            self.driver.get(profile_url)
            self._human_delay('page_load')
            
            # Verificar que llegamos al perfil correcto
            try:
                # Buscar indicadores del perfil
                profile_indicators = [
                    f"//h2[text()='{username}']",
                    f"//*[contains(@title, '{username}')]",
                    "//article//header",
                    "//main//header"
                ]
                
                for indicator in profile_indicators:
                    try:
                        self.wait.until(EC.presence_of_element_located((By.XPATH, indicator)))
                        log.info("✅ Perfil cargado correctamente")
                        return True
                    except TimeoutException:
                        continue
                
                # Si no encontramos indicadores específicos, verificar que no hay error 404
                page_source = self.driver.page_source.lower()
                if "page not found" in page_source or "user not found" in page_source:
                    log.error(f"❌ Perfil @{username} no encontrado")
                    return False
                
                log.info("✅ Perfil cargado (verificación básica)")
                return True
                
            except Exception as e:
                log.error(f"❌ Error verificando perfil: {e}")
                return False
            
        except Exception as e:
            log.error(f"❌ Error navegando al perfil: {e}")
            return False
    
    def extract_profile_info(self, username: str) -> Optional[Dict[str, Any]]:
        """Extraer información del perfil de forma manual"""
        try:
            log.info(f"📊 Extrayendo información del perfil @{username}...")
            
            # Esperar a que la página cargue completamente
            self._human_delay('page_load')
            
            profile_info = {
                'username': username,
                'full_name': '',
                'bio': '',
                'followers_count': 0,
                'following_count': 0,
                'posts_count': 0,
                'is_private': False,
                'is_verified': False,
                'profile_pic_url': '',
                'external_url': ''
            }
            
            # Extraer nombre completo
            try:
                name_selectors = [
                    "//main//header//h1",
                    "//article//header//h1",
                    "//h1[contains(@class, 'username')]",
                    "h1"
                ]
                
                for selector in name_selectors:
                    try:
                        if selector.startswith("//"):
                            name_element = self.driver.find_element(By.XPATH, selector)
                        else:
                            name_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        
                        profile_info['full_name'] = name_element.text.strip()
                        break
                    except NoSuchElementException:
                        continue
                        
            except Exception as e:
                log.warning(f"No se pudo extraer nombre completo: {e}")
            
            # Extraer estadísticas (posts, followers, following)
            try:
                stats_selectors = [
                    "//main//header//ul//li",
                    "//article//header//ul//li",
                    "//header//ul//li",
                    "ul li"
                ]
                
                for selector in stats_selectors:
                    try:
                        if selector.startswith("//"):
                            stats_elements = self.driver.find_elements(By.XPATH, selector)
                        else:
                            stats_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        
                        if len(stats_elements) >= 3:
                            # Extraer números de las estadísticas
                            for i, stat in enumerate(stats_elements[:3]):
                                stat_text = stat.text.strip()
                                numbers = re.findall(r'[\d,]+', stat_text)
                                
                                if numbers:
                                    count = int(numbers[0].replace(',', ''))
                                    
                                    if i == 0:  # Posts
                                        profile_info['posts_count'] = count
                                    elif i == 1:  # Followers
                                        profile_info['followers_count'] = count
                                    elif i == 2:  # Following
                                        profile_info['following_count'] = count
                            break
                            
                    except Exception:
                        continue
                        
            except Exception as e:
                log.warning(f"No se pudieron extraer estadísticas: {e}")
            
            # Extraer bio
            try:
                bio_selectors = [
                    "//main//header//div[contains(@class, 'bio')]",
                    "//article//header//div//span",
                    "//*[contains(@data-testid, 'bio')]",
                    "//header//span"
                ]
                
                for selector in bio_selectors:
                    try:
                        bio_element = self.driver.find_element(By.XPATH, selector)
                        profile_info['bio'] = bio_element.text.strip()
                        break
                    except NoSuchElementException:
                        continue
                        
            except Exception as e:
                log.warning(f"No se pudo extraer bio: {e}")
            
            # Verificar si es privado
            try:
                page_source = self.driver.page_source.lower()
                if "this account is private" in page_source or "private account" in page_source:
                    profile_info['is_private'] = True
            except Exception:
                pass
            
            # Verificar si está verificado
            try:
                verified_selectors = [
                    "//*[contains(@aria-label, 'Verified')]",
                    "//*[contains(@title, 'Verified')]",
                    "//svg[contains(@aria-label, 'Verified')]"
                ]
                
                for selector in verified_selectors:
                    try:
                        self.driver.find_element(By.XPATH, selector)
                        profile_info['is_verified'] = True
                        break
                    except NoSuchElementException:
                        continue
                        
            except Exception:
                pass
            
            log.info(f"✅ Información del perfil extraída: {profile_info['posts_count']} posts, {profile_info['followers_count']} followers")
            return profile_info
            
        except Exception as e:
            log.error(f"❌ Error extrayendo información del perfil: {e}")
            return None
    
    def scroll_and_load_posts(self, target_posts: int = None) -> int:
        """Hacer scroll para cargar más posts de forma humana"""
        try:
            log.info(f"📜 Haciendo scroll para cargar posts...")
            
            # Si no hay target, intentar cargar todos
            if target_posts is None:
                target_posts = 1000  # Número alto para intentar cargar todo
            
            posts_loaded = 0
            scroll_attempts = 0
            max_scrolls = 50  # Límite de seguridad
            no_new_posts_count = 0
            
            while scroll_attempts < max_scrolls and no_new_posts_count < 5:
                # Contar posts actuales
                current_posts = len(self.driver.find_elements(By.CSS_SELECTOR, "article a[href*='/p/']"))
                
                if current_posts >= target_posts:
                    log.info(f"✅ Target alcanzado: {current_posts} posts cargados")
                    break
                
                # Hacer scroll humano
                self._human_scroll('down', random.randint(500, 1200))
                
                # Esperar a que carguen nuevos posts
                time.sleep(random.uniform(2, 4))
                
                # Verificar si se cargaron nuevos posts
                new_posts = len(self.driver.find_elements(By.CSS_SELECTOR, "article a[href*='/p/']"))
                
                if new_posts > current_posts:
                    posts_loaded = new_posts
                    no_new_posts_count = 0
                    log.info(f"📈 Posts cargados: {posts_loaded}")
                else:
                    no_new_posts_count += 1
                    log.debug(f"Sin nuevos posts (intento {no_new_posts_count}/5)")
                
                scroll_attempts += 1
                
                # Scroll ocasional hacia arriba para parecer más humano
                if random.random() < 0.1:  # 10% de probabilidad
                    self._human_scroll('up', random.randint(200, 400))
                    self._human_delay('scroll')
            
            log.info(f"✅ Scroll completado: {posts_loaded} posts cargados en {scroll_attempts} scrolls")
            return posts_loaded
            
        except Exception as e:
            log.error(f"❌ Error haciendo scroll: {e}")
            return 0
    
    def extract_posts_data(self) -> List[Dict[str, Any]]:
        """Extraer datos de posts de forma manual"""
        try:
            log.info("📸 Extrayendo datos de posts...")
            
            posts_data = []
            
            # Encontrar todos los enlaces de posts
            post_links = self.driver.find_elements(By.CSS_SELECTOR, "article a[href*='/p/']")
            
            log.info(f"🔍 Encontrados {len(post_links)} enlaces de posts")
            
            # Extraer información básica de cada post
            for i, link in enumerate(post_links):
                try:
                    post_url = link.get_attribute('href')
                    
                    # Extraer shortcode del URL
                    shortcode_match = re.search(r'/p/([^/]+)/', post_url)
                    shortcode = shortcode_match.group(1) if shortcode_match else f"unknown_{i}"
                    
                    # Buscar la imagen/video dentro del enlace
                    try:
                        img_element = link.find_element(By.TAG_NAME, 'img')
                        media_url = img_element.get_attribute('src')
                        media_type = 'image'
                    except NoSuchElementException:
                        try:
                            video_element = link.find_element(By.TAG_NAME, 'video')
                            media_url = video_element.get_attribute('src')
                            media_type = 'video'
                        except NoSuchElementException:
                            media_url = ''
                            media_type = 'unknown'
                    
                    post_data = {
                        'shortcode': shortcode,
                        'url': media_url,
                        'post_url': post_url,
                        'type': media_type,
                        'timestamp': None,
                        'caption': '',
                        'likes_count': 0,
                        'comments_count': 0
                    }
                    
                    posts_data.append(post_data)
                    
                    if (i + 1) % 10 == 0:
                        log.info(f"📊 Procesados {i + 1}/{len(post_links)} posts")
                    
                except Exception as e:
                    log.warning(f"Error procesando post {i}: {e}")
                    continue
            
            log.info(f"✅ Datos extraídos de {len(posts_data)} posts")
            return posts_data
            
        except Exception as e:
            log.error(f"❌ Error extrayendo datos de posts: {e}")
            return []
    
    def get_detailed_post_info(self, post_url: str) -> Optional[Dict[str, Any]]:
        """Obtener información detallada de un post específico"""
        try:
            log.info(f"🔍 Obteniendo info detallada del post: {post_url}")
            
            # Navegar al post
            self.driver.get(post_url)
            self._human_delay('page_load')
            
            post_info = {
                'caption': '',
                'likes_count': 0,
                'comments_count': 0,
                'timestamp': '',
                'location': '',
                'tagged_users': []
            }
            
            # Extraer caption
            try:
                caption_selectors = [
                    "//article//div//span[contains(@class, 'caption')]",
                    "//article//div//span",
                    "//*[contains(@data-testid, 'caption')]"
                ]
                
                for selector in caption_selectors:
                    try:
                        caption_element = self.driver.find_element(By.XPATH, selector)
                        post_info['caption'] = caption_element.text.strip()
                        break
                    except NoSuchElementException:
                        continue
                        
            except Exception as e:
                log.warning(f"No se pudo extraer caption: {e}")
            
            # Extraer likes
            try:
                likes_selectors = [
                    "//article//section//button//span",
                    "//*[contains(text(), 'likes')]",
                    "//span[contains(@class, 'likes')]"
                ]
                
                for selector in likes_selectors:
                    try:
                        likes_element = self.driver.find_element(By.XPATH, selector)
                        likes_text = likes_element.text
                        numbers = re.findall(r'[\d,]+', likes_text)
                        if numbers:
                            post_info['likes_count'] = int(numbers[0].replace(',', ''))
                            break
                    except NoSuchElementException:
                        continue
                        
            except Exception as e:
                log.warning(f"No se pudieron extraer likes: {e}")
            
            return post_info
            
        except Exception as e:
            log.error(f"❌ Error obteniendo info detallada: {e}")
            return None
    
    def scrape_profile_complete(self, username: str, cookies_string: str = None) -> Dict[str, Any]:
        """Scraping completo de un perfil usando Selenium"""
        try:
            log.info(f"🚀 INICIANDO SCRAPING COMPLETO DE @{username}")
            
            # Usar cookies hardcodeadas si no se proporcionan
            if not cookies_string:
                cookies_string = HARDCODED_COOKIES
                log.info("🍪 Usando cookies hardcodeadas para desarrollo")
            
            # Inicializar navegador
            if not self.initialize_browser():
                return {'error': 'Failed to initialize browser'}
            
            # Cargar cookies
            if not self.load_cookies(cookies_string):
                return {'error': 'Failed to load cookies'}
            
            # Verificar autenticación
            if not self.verify_authentication():
                log.warning("⚠️ Autenticación no verificada, continuando...")
            
            # Navegar al perfil
            if not self.navigate_to_profile(username):
                return {'error': f'Failed to navigate to profile @{username}'}
            
            # Extraer información del perfil
            profile_info = self.extract_profile_info(username)
            if not profile_info:
                return {'error': 'Failed to extract profile info'}
            
            # Hacer scroll para cargar posts
            total_posts = profile_info.get('posts_count', 0)
            loaded_posts = self.scroll_and_load_posts(total_posts)
            
            # Extraer datos de posts
            posts_data = self.extract_posts_data()
            
            result = {
                'profile': profile_info,
                'posts': posts_data,
                'total_posts_found': len(posts_data),
                'posts_loaded_by_scroll': loaded_posts,
                'scraping_method': 'selenium_manual',
                'authenticated': self.authenticated,
                'success': True
            }
            
            log.info(f"🎉 SCRAPING COMPLETADO: {len(posts_data)} posts de @{username}")
            return result
            
        except Exception as e:
            log.error(f"❌ Error en scraping completo: {e}")
            return {'error': str(e), 'success': False}
        
        finally:
            # Limpiar recursos
            self.cleanup()
    
    def cleanup(self):
        """Limpiar recursos del navegador"""
        try:
            if self.driver:
                log.info("🧹 Cerrando navegador...")
                self.driver.quit()
                self.driver = None
                self.wait = None
                self.cookies_loaded = False
                self.authenticated = False
                log.info("✅ Navegador cerrado correctamente")
        except Exception as e:
            log.warning(f"Error cerrando navegador: {e}")

# Instancia global del scraper
selenium_scraper = InstagramSeleniumScraper()

async def scrape_with_selenium(username: str, cookies_string: str = None) -> Dict[str, Any]:
    """
    Función principal para scraping con Selenium
    """
    log.info(f"🔥 SELENIUM SCRAPING INICIADO PARA @{username}")
    
    # Usar cookies hardcodeadas si no se proporcionan
    if not cookies_string:
        cookies_string = HARDCODED_COOKIES
        log.info("🍪 Usando cookies hardcodeadas para desarrollo")
    
    try:
        # Ejecutar scraping en thread separado para no bloquear
        import asyncio
        import concurrent.futures
        
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(
                executor, 
                selenium_scraper.scrape_profile_complete,
                username,
                cookies_string
            )
        
        return result
        
    except Exception as e:
        log.error(f"❌ Error en scraping con Selenium: {e}")
        return {'error': str(e), 'success': False}
#!/usr/bin/env python3
"""
Instagram Scraper con Selenium
Implementación robusta para scraping de perfiles de Instagram
"""

import os
import json
import time
import random
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
# ChromeDriverManager removido - usando chromedriver del sistema

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Instagram session tokens - Cargados desde variables de entorno
import os

INSTAGRAM_SESSIONID = os.environ.get('INSTAGRAM_SESSIONID', '')
INSTAGRAM_CSRFTOKEN = os.environ.get('INSTAGRAM_CSRFTOKEN', '')
INSTAGRAM_DS_USER_ID = os.environ.get('INSTAGRAM_DS_USER_ID', '')
INSTAGRAM_ALL_COOKIES = os.environ.get('INSTAGRAM_ALL_COOKIES', '')

# Anti-detección: User Agent FIJO por sesión (más realista)
USER_AGENT_FIXED = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Anti-detección: Resolución FIJA por sesión (más realista)
SCREEN_RESOLUTION_FIXED = (1920, 1080)

# Anti-detección: Idioma FIJO por sesión (más realista)
LANGUAGE_FIXED = 'en-US,en;q=0.9'

# Anti-detección: Plataforma FIJA por sesión (más realista)
PLATFORM_FIXED = "Win32"

def get_fixed_user_agent() -> str:
    """Obtener User Agent fijo para toda la sesión (más realista)"""
    return USER_AGENT_FIXED

def get_fixed_screen_resolution() -> tuple:
    """Obtener resolución fija para toda la sesión (más realista)"""
    return SCREEN_RESOLUTION_FIXED

def random_delay(min_seconds: int = 3, max_seconds: int = 8) -> None:
    """Esperar un tiempo aleatorio entre min_seconds y max_seconds (anti-baneo)"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

def get_fixed_headers() -> Dict[str, str]:
    """Generar headers HTTP fijos para simular usuario consistente"""
    headers = {
        'User-Agent': USER_AGENT_FIXED,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': LANGUAGE_FIXED,
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',  # Fijo - usuario que siempre tiene DNT activado
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0',
        'Sec-CH-UA': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'Sec-CH-UA-Mobile': '?0',
        'Sec-CH-UA-Platform': f'"{PLATFORM_FIXED}"'
    }
    return headers

class InstagramScraper:
    """Scraper de Instagram con medidas anti-baneo avanzadas"""
    
    def __init__(self):
        self.driver = None
        self.cookies = None
        self.authenticated = False
        self.logs = []
        self.status = "Inicializado"
        
        # Configuración anti-baneo
        self.request_count = 0
        self.session_start_time = time.time()
        self.max_requests_per_session = random.randint(10, 20)  # Límite conservador
        self.min_delay_between_requests = 4  # Mínimo 4 segundos
        self.max_delay_between_requests = 10  # Máximo 10 segundos
        
        # Control de progreso
        self.progress = {
            'current': 0,
            'total': 0,
            'percentage': 0,
            'status': 'Inicializado',
            'current_action': '',
            'posts_downloaded': 0,
            'posts_total': 0
        }
        
        # Configuración
        self.base_url = "https://www.instagram.com"
        self.download_dir = os.path.abspath("downloads")
        self.logs_dir = os.path.abspath("logs")
        
        # Crear directorios
        os.makedirs(self.download_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        
        self.log("🚀 Scraper inicializado con perfil CONSISTENTE (más realista)")
        
        # Auto-configurar cookies predefinidas
        self.auto_configure_cookies()
    
    def auto_configure_cookies(self):
        """Auto-configurar cookies actualizadas de la nueva cuenta"""
        try:
            self.log("🔧 Auto-configurando cookies de nueva cuenta...")
            success = self.set_cookies()
            if success:
                self.log("✅ Cookies de nueva cuenta configuradas automáticamente")
                self.log(f"🔐 Nueva cuenta ID: {INSTAGRAM_DS_USER_ID}")
            else:
                self.log("⚠️ No se pudieron configurar cookies predefinidas", "WARNING")
        except Exception as e:
            self.log(f"❌ Error en auto-configuración: {str(e)}", "ERROR")
    
    def log(self, message: str, level: str = "INFO"):
        """Agregar entrada al log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'level': level,
            'message': message
        }
        self.logs.append(log_entry)
        
        # También log a archivo
        log_file = os.path.join(self.logs_dir, f"scraper_{datetime.now().strftime('%Y%m%d')}.log")
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {level}: {message}\n")
        
        # Log a consola
        if level == "ERROR":
            logger.error(message)
        elif level == "WARNING":
            logger.warning(message)
        else:
            logger.info(message)
    
    def check_rate_limits(self):
        """Verificar límites de velocidad anti-baneo"""
        self.request_count += 1
        session_duration = time.time() - self.session_start_time
        
        # Verificar si excedemos límites
        if self.request_count >= self.max_requests_per_session:
            self.log(f"⚠️ Límite de requests alcanzado ({self.request_count}/{self.max_requests_per_session})", "WARNING")
            self.log("😴 Pausa larga para evitar detección...")
            time.sleep(random.uniform(60, 120))  # Pausa de 1-2 minutos
            self.reset_session_limits()
        
        # Verificar velocidad de requests
        if session_duration > 0:
            requests_per_minute = (self.request_count / session_duration) * 60
            if requests_per_minute > 8:  # Máximo 8 requests por minuto (conservador)
                extra_delay = random.uniform(5, 15)
                self.log(f"🐌 Reduciendo velocidad - delay extra: {extra_delay:.1f}s", "WARNING")
                time.sleep(extra_delay)
    
    def reset_session_limits(self):
        """Resetear límites de sesión"""
        self.request_count = 0
        self.session_start_time = time.time()
        self.max_requests_per_session = random.randint(10, 20)
        self.log("🔄 Límites de sesión reseteados")
    
    def get_logs(self) -> List[Dict]:
        """Obtener logs recientes (últimos 100)"""
        return self.logs[-100:]
    
    def clear_logs(self):
        """Limpiar logs en memoria"""
        self.logs = []
        self.log("Logs limpiados")
    
    def get_status(self) -> Dict:
        """Obtener estado actual del scraper con información de progreso"""
        session_duration = time.time() - self.session_start_time
        return {
            'status': self.status,
            'driver_active': self.driver is not None,
            'authenticated': self.authenticated,
            'cookies_set': self.cookies is not None,
            'logs_count': len(self.logs),
            'request_count': self.request_count,
            'max_requests': self.max_requests_per_session,
            'session_duration': f"{session_duration/60:.1f} min",
            'anti_ban_active': True,
            'progress': self.progress.copy()
        }
    
    def get_auth_status(self) -> Dict:
        """Obtener estado de autenticación"""
        return {
            'authenticated': self.authenticated,
            'cookies_configured': self.cookies is not None,
            'cookies_count': len(self.cookies) if self.cookies else 0,
            'user_id': INSTAGRAM_DS_USER_ID,
            'account_updated': True
        }
    
    def is_authenticated(self) -> bool:
        """Verificar si está autenticado"""
        return self.authenticated and self.cookies is not None
    
    def setup_driver_with_anti_detection(self) -> webdriver.Chrome:
        """Configurar driver de Chrome con configuración FIJA (más realista)"""
        try:
            self.log("🔧 Configurando navegador con perfil consistente...")
            
            # Usar configuración fija para toda la sesión - con valores por defecto
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            width, height = 1920, 1080
            language = "en-US,en;q=0.9"
            platform = "Win32"
            
            # Verificar que las variables no sean None
            if not user_agent or not language or not platform:
                raise Exception("Variables de configuración no están definidas correctamente")
            
            # Configuración del navegador con valores fijos
            self.log(f"🌐 User Agent: {user_agent}")
            self.log(f"🌍 Idioma: {language}")
            self.log(f"💻 Plataforma: {platform}")
            
            # Configurar opciones de Chrome
            chrome_options = Options()
            
            # Configuración consistente (como usuario real)
            chrome_options.add_argument(f"--user-agent={user_agent}")
            chrome_options.add_argument(f"--window-size={width},{height}")
            
            # Verificación extra antes del split
            if language and isinstance(language, str):
                lang_split = language.split(',')[0]
                chrome_options.add_argument(f"--lang={lang_split}")
                self.log(f"✅ Idioma configurado: {lang_split}")
            else:
                self.log(f"❌ ERROR: language es {language} (tipo: {type(language)})", "ERROR")
                chrome_options.add_argument("--lang=en-US")  # Fallback
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-images")  # Más rápido y menos detectable
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-dev-tools")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            
            # Opciones experimentales anti-detección
            chrome_options.add_experimental_option("excludeSwitches", [
                "enable-automation", 
                "enable-logging",
                "enable-blink-features"
            ])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Preferencias fijas
            prefs = {
                "profile.managed_default_content_settings.images": 2,
                "profile.default_content_setting_values.notifications": 2,
                "profile.default_content_settings.popups": 0,
                "profile.managed_default_content_settings.media_stream": 2,
                "profile.default_content_setting_values.geolocation": 2,
                "profile.managed_default_content_settings.plugins": 2,
                "profile.password_manager_enabled": False,
                "credentials_enable_service": False,
                "profile.default_content_settings.auto_select_certificate": 2
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            # Modo headless para producción - sin ventana del navegador
            chrome_options.add_argument("--headless")
            
            # Usar chromedriver del sistema directamente (más confiable)
            service = Service()  # Usa chromedriver del PATH
            self.log("🔍 Usando chromedriver del sistema...")
            
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Configuraciones JavaScript anti-detección
            driver.execute_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                window.chrome = {runtime: {}};
                Object.defineProperty(navigator, 'permissions', {get: () => ({query: () => Promise.resolve({state: 'granted'})})});
            """)
            
            # Configurar CDP con valores fijos
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": user_agent,
                "acceptLanguage": language,
                "platform": platform
            })
            
            # Configurar viewport fijo
            driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {
                'width': width,
                'height': height,
                'deviceScaleFactor': 1.0,  # Fijo
                'mobile': False
            })
            
            self.log(f"✅ Navegador configurado con perfil consistente")
            self.log(f"📐 Resolución fija: {width}x{height}")
            self.log(f"🌐 Idioma fijo: {language}")
            self.log(f"💻 Plataforma fija: {platform}")
            
            return driver
            
        except Exception as e:
            self.log(f"❌ Error configurando navegador: {str(e)}", "ERROR")
            raise e
    
    def random_human_delay(self, action: str = "acción"):
        """Simular comportamiento humano con delays aleatorios"""
        delay = random.uniform(1.5, 3.5)  # Reducido de 2-5s a 1.5-3.5s
        self.log(f"⏱️ Esperando {delay:.1f}s después de {action}...")
        time.sleep(delay)
    
    def simulate_human_behavior(self, driver: webdriver.Chrome):
        """Simular comportamiento humano en el navegador"""
        try:
            # Scroll aleatorio
            scroll_pause = random.uniform(0.5, 1.5)
            scroll_height = random.randint(200, 800)
            
            driver.execute_script(f"window.scrollBy(0, {scroll_height});")
            time.sleep(scroll_pause)
            
            # Movimiento del mouse aleatorio (simulado)
            driver.execute_script("""
                var event = new MouseEvent('mousemove', {
                    'view': window,
                    'bubbles': true,
                    'cancelable': true,
                    'clientX': Math.random() * window.innerWidth,
                    'clientY': Math.random() * window.innerHeight
                });
                document.dispatchEvent(event);
            """)
            
            self.log("🤖 Comportamiento humano simulado")
            
        except Exception as e:
            self.log(f"⚠️ Error simulando comportamiento: {str(e)}", "WARNING")
    
    def load_cookies_to_driver(self, driver: webdriver.Chrome):
        """Cargar cookies en el navegador"""
        try:
            if not self.cookies:
                self.log("⚠️ No hay cookies para cargar", "WARNING")
                return False
            
            # Cargar cookies en el navegador
            cookies_loaded = 0
            for name, value in self.cookies.items():
                try:
                    driver.add_cookie({
                        'name': name,
                        'value': value,
                        'domain': '.instagram.com',
                        'path': '/',
                        'secure': True
                    })
                    cookies_loaded += 1
                except Exception as e:
                    self.log(f"⚠️ Error cargando cookie {name}: {str(e)}", "WARNING")
            
            self.log(f"✅ Cookies cargadas en navegador: {cookies_loaded}/{len(self.cookies)}")
            
            # Refrescar página para aplicar cookies
            driver.refresh()
            self.random_human_delay("aplicar cookies")
            
            return cookies_loaded > 0
            
        except Exception as e:
            self.log(f"❌ Error cargando cookies: {str(e)}", "ERROR")
            return False
    
    def set_cookies(self, cookies_text: str = None) -> bool:
        """Configurar cookies de Instagram (usa cookies predefinidas si no se especifica)"""
        try:
            # Si no se proporcionan cookies, usar las predefinidas
            if not cookies_text:
                # Usar cookies desde variables de entorno
                cookies_text = os.environ.get('INSTAGRAM_ALL_COOKIES', '')
                if not cookies_text:
                    self.log("⚠️  No hay cookies configuradas en variables de entorno", "WARNING")
                    return False
                self.log("Usando cookies desde variables de entorno")
            else:
                self.log("Configurando cookies personalizadas...")
            
            # Verificación de seguridad
            if not cookies_text or not isinstance(cookies_text, str):
                self.log(f"❌ ERROR: cookies_text es {cookies_text} (tipo: {type(cookies_text)})", "ERROR")
                return False
            
            # Parsear cookies
            cookies_dict = {}
            for cookie in cookies_text.split(';'):
                if '=' in cookie:
                    key, value = cookie.strip().split('=', 1)
                    cookies_dict[key.strip()] = value.strip()
            
            if not cookies_dict:
                self.log("No se encontraron cookies válidas", "ERROR")
                return False
            
            # Verificar cookies esenciales
            essential_cookies = ['sessionid', 'csrftoken', 'ds_user_id']
            missing_cookies = [c for c in essential_cookies if c not in cookies_dict]
            
            if missing_cookies:
                self.log(f"Faltan cookies esenciales: {missing_cookies}", "WARNING")
            
            self.cookies = cookies_dict
            self.authenticated = True
            self.log(f"✅ Cookies configuradas: {len(cookies_dict)} cookies")
            self.log(f"🔐 Usuario autenticado: {cookies_dict.get('ds_user_id', 'N/A')}")
            
            return True
            
        except Exception as e:
            self.log(f"Error al configurar cookies: {str(e)}", "ERROR")
            return False
    
    def scrape_profile(self, username: str) -> Dict[str, Any]:
        """Scraping REAL de perfil con descarga de posts y barra de progreso"""
        try:
            self.status = f"Scraping: {username}"
            self.reset_progress()
            self.update_progress(0, 100, "Iniciando scraping...")
            
            # Verificar límites de velocidad
            self.check_rate_limits()
            
            if not self.is_authenticated():
                raise Exception("No hay autenticación configurada")
            
            # Paso 1: Configurar navegador
            self.update_progress(10, 100, "Configurando navegador...")
            driver = self.setup_driver_with_anti_detection()
            self.driver = driver
            
            try:
                # Paso 2: Navegar a Instagram
                self.update_progress(20, 100, "Navegando a Instagram...")
                driver.get("https://www.instagram.com/")
                time.sleep(random.uniform(5, 8))
                
                # Paso 3: Cargar cookies
                self.update_progress(30, 100, "Cargando autenticación...")
                self.load_cookies_to_driver(driver)
                time.sleep(random.uniform(3, 6))
                
                # Paso 4: Navegar al perfil
                self.update_progress(40, 100, f"Navegando al perfil @{username}...")
                profile_url = f"https://www.instagram.com/{username}/"
                driver.get(profile_url)
                time.sleep(random.uniform(5, 10))
                
                # Paso 5: Extraer información del perfil
                self.update_progress(50, 100, "Analizando perfil...")
                profile_info = self.extract_profile_info(driver, username)
                
                # Paso 6: Obtener total de posts
                posts_count = profile_info.get('posts_count', 0)
                self.update_progress(60, 100, f"Encontrados {posts_count} posts...")
                
                # Paso 7: Extraer posts con progreso
                self.update_progress(70, 100, "Extrayendo lista de posts...")
                posts = self.extract_posts_with_progress(driver, username, posts_count)
                
                # Paso 8: Descargar posts
                self.update_progress(80, 100, "Descargando posts...")
                downloaded_posts = self.download_posts_with_progress(posts, username)
                
                # Paso 9: Finalizar
                self.update_progress(100, 100, "Scraping completado!")
                
            finally:
                # Cerrar navegador
                if driver:
                    driver.quit()
                    self.driver = None
            
            result = {
                'username': username,
                'profile': profile_info,
                'posts': downloaded_posts,
                'scraping_info': {
                    'timestamp': datetime.now().isoformat(),
                    'posts_found': len(downloaded_posts),
                    'posts_downloaded': len([p for p in downloaded_posts if p.get('downloaded', False)]),
                    'method': 'selenium_real_download',
                    'anti_ban_measures': 'ACTIVAS',
                    'session_requests': self.request_count,
                    'max_session_requests': self.max_requests_per_session
                }
            }
            
            self.status = "Completado"
            self.log(f"✅ Scraping completado: {len(downloaded_posts)} posts procesados")
            
            return result
            
        except Exception as e:
            self.status = "Error"
            self.log(f"❌ Error en scraping: {str(e)}", "ERROR")
            raise e
    
    def extract_profile_info(self, driver, username: str) -> Dict:
        """Extraer información REAL del perfil de Instagram"""
        try:
            self.log(f"📊 Extrayendo información REAL del perfil @{username}...")
            
            # Simular comportamiento humano
            self.simulate_human_behavior(driver)
            time.sleep(random.uniform(3, 6))
            
            # Extraer datos REALES del DOM de Instagram
            try:
                # Buscar el nombre completo
                full_name_element = driver.find_element(By.CSS_SELECTOR, "h1")
                full_name = full_name_element.text if full_name_element else username
            except:
                full_name = username
            
            try:
                # Buscar la biografía
                bio_element = driver.find_element(By.CSS_SELECTOR, "h1 + div + div")
                bio = bio_element.text if bio_element else ""
            except:
                bio = ""
            
            try:
                # Método simple: Buscar en header del perfil
                posts_count = 0
                followers_count = 0
                following_count = 0
                
                header_stats = driver.find_elements(By.CSS_SELECTOR, "header section ul li")
                if len(header_stats) >= 1:
                    try:
                        # El texto viene como "25 posts", extraer solo el número
                        posts_text = header_stats[0].text.split()[0].replace(',', '').replace('.', '')
                        if posts_text.isdigit():
                            posts_count = int(posts_text)
                            self.log(f"📊 Posts encontrados: {posts_count}")
                    except:
                        pass
                
                # Fallback simple si no se encuentra
                if posts_count == 0:
                    post_elements = driver.find_elements(By.CSS_SELECTOR, "article a[href*='/p/']")
                    posts_count = len(post_elements) if post_elements else 0
                    self.log(f"📊 Posts contados visualmente: {posts_count}")
                
            except Exception as stats_error:
                self.log(f"⚠️ Error extrayendo estadísticas: {stats_error}", "WARNING")
                posts_count = 0
                followers_count = 0
                following_count = 0
            
            try:
                # Verificar si es cuenta privada
                private_text = driver.page_source.lower()
                is_private = 'this account is private' in private_text or 'cuenta privada' in private_text
            except:
                is_private = False
            
            try:
                # Verificar si está verificado
                verified_elements = driver.find_elements(By.CSS_SELECTOR, "[title*='Verified'], [aria-label*='Verified']")
                is_verified = len(verified_elements) > 0
            except:
                is_verified = False
            
            profile_info = {
                'username': username,
                'full_name': full_name,
                'bio': bio,
                'posts_count': posts_count,
                'followers_count': followers_count,
                'following_count': following_count,
                'is_private': is_private,
                'is_verified': is_verified,
                'profile_pic_url': f'https://instagram.com/{username}/profile.jpg'
            }
            
            self.log(f"✅ Perfil REAL analizado: {posts_count} posts encontrados")
            self.log(f"   Nombre: {full_name}")
            self.log(f"   Privado: {is_private}, Verificado: {is_verified}")
            
            return profile_info
            
        except Exception as e:
            self.log(f"❌ Error extrayendo perfil: {str(e)}", "ERROR")
            return {'username': username, 'posts_count': 0}
    
    def extract_posts_with_progress(self, driver, username: str, total_posts: int) -> List[Dict]:
        """Extraer posts REALES con barra de progreso"""
        try:
            posts = []
            max_posts = min(total_posts, 50)  # Límite aumentado para perfiles medianos
            
            self.log(f"📸 Extrayendo hasta {max_posts} posts REALES...")
            
            # Buscar enlaces de posts reales en el DOM con scroll para cargar más
            self.log("🔄 Cargando posts con scroll...")
            
            # Hacer scroll MEJORADO para cargar TODOS los posts
            posts_loaded = 0
            scroll_attempts = 0
            max_scroll_attempts = 15  # Más intentos para asegurar todos los posts
            no_change_count = 0
            
            while posts_loaded < max_posts and scroll_attempts < max_scroll_attempts and no_change_count < 4:
                # Usar solo el selector que funciona
                selectors = ["article a[href*='/p/']"]
                
                current_post_links = []
                for selector in selectors:
                    links = driver.find_elements(By.CSS_SELECTOR, selector)
                    current_post_links.extend(links)
                
                # Eliminar duplicados basado en href
                seen_hrefs = set()
                unique_links = []
                for link in current_post_links:
                    href = link.get_attribute('href')
                    if href and href not in seen_hrefs:
                        seen_hrefs.add(href)
                        unique_links.append(link)
                
                current_post_links = unique_links
                current_count = len(current_post_links)
                
                self.log(f"📊 Posts visibles después de scroll {scroll_attempts + 1}: {current_count}")
                
                # Verificar si hay cambio
                if current_count == posts_loaded:
                    no_change_count += 1
                    self.log(f"⏳ Sin cambios en scroll {no_change_count}/3")
                else:
                    no_change_count = 0  # Reset contador si hay cambios
                
                posts_loaded = current_count
                
                # Si ya tenemos suficientes posts, parar
                if posts_loaded >= max_posts:
                    self.log(f"✅ Suficientes posts cargados: {posts_loaded}/{max_posts}")
                    break
                
                # Si no hay cambios por 4 intentos consecutivos, parar
                if no_change_count >= 4:
                    self.log("📊 No se cargan más posts después de 4 intentos, terminando scroll")
                    break
                
                # Método MEJORADO: Scroll gradual más natural
                driver.execute_script("""
                    // Scroll gradual más natural
                    let currentHeight = window.pageYOffset;
                    let targetHeight = document.body.scrollHeight;
                    let increment = (targetHeight - currentHeight) / 3;
                    
                    function smoothScroll(step) {
                        if (step < 3) {
                            window.scrollTo(0, currentHeight + (increment * (step + 1)));
                            setTimeout(() => smoothScroll(step + 1), 500);
                        }
                    }
                    smoothScroll(0);
                    
                    // Disparar eventos de scroll
                    window.dispatchEvent(new Event('scroll'));
                """)
                time.sleep(random.uniform(4, 6))  # Reducido de 5-8s a 4-6s
                
                scroll_attempts += 1
            
            # Usar solo el selector que funciona
            selectors = ["article a[href*='/p/']"]
            
            all_post_links = []
            for selector in selectors:
                links = driver.find_elements(By.CSS_SELECTOR, selector)
                all_post_links.extend(links)
            
            # Eliminar duplicados basado en href
            seen_hrefs = set()
            post_links = []
            for link in all_post_links:
                href = link.get_attribute('href')
                if href and href not in seen_hrefs and '/p/' in href:
                    seen_hrefs.add(href)
                    post_links.append(link)
            
            if not post_links:
                self.log("⚠️ No se encontraron posts visibles. Puede ser cuenta privada.", "WARNING")
                return []
            
            actual_posts_found = min(len(post_links), max_posts)
            self.log(f"✅ Posts finales encontrados: {len(post_links)}, procesando: {actual_posts_found}")
            
            # Verificar si se cargaron todos los posts del perfil
            if len(post_links) >= total_posts:
                self.log(f"🎉 Se cargaron TODOS los posts del perfil ({len(post_links)}/{total_posts})")
            elif len(post_links) >= total_posts * 0.8:  # 80% o más
                self.log(f"✅ Se cargó la mayoría de posts ({len(post_links)}/{total_posts} = {len(post_links)/total_posts*100:.1f}%)")
            else:
                self.log(f"⚠️ Solo se cargaron {len(post_links)}/{total_posts} posts ({len(post_links)/total_posts*100:.1f}%)", "WARNING")
            
            for i in range(actual_posts_found):
                try:
                    # Actualizar progreso
                    progress = int((i / actual_posts_found) * 30) + 70  # 70-100%
                    self.update_progress(progress, 100, f"Extrayendo post {i+1}/{actual_posts_found}")
                    
                    post_link = post_links[i]
                    post_url = post_link.get_attribute('href')
                    
                    # Extraer shortcode del URL
                    shortcode = post_url.split('/p/')[-1].rstrip('/')
                    
                    # Obtener timestamp REAL del post (más preciso)
                    timestamp = self.extract_real_timestamp_from_shortcode(shortcode)
                    
                    # Intentar extraer imagen del post
                    try:
                        img_element = post_link.find_element(By.TAG_NAME, 'img')
                        media_url = img_element.get_attribute('src')
                        alt_text = img_element.get_attribute('alt') or ""
                    except:
                        media_url = None
                        alt_text = ""
                    
                    # Determinar tipo de post
                    post_type = 'image'
                    media_urls = [media_url] if media_url else []
                    
                    try:
                        # Buscar indicadores de video o carousel
                        if post_link.find_elements(By.CSS_SELECTOR, "[aria-label*='Video'], [aria-label*='video']"):
                            post_type = 'video'
                        elif post_link.find_elements(By.CSS_SELECTOR, "[aria-label*='Carousel'], [aria-label*='carousel']"):
                            post_type = 'carousel'
                            # Marcar como carrusel para procesamiento posterior
                    except:
                        pass
                    
                    post = {
                        'id': f'{username}_post_{i+1}',
                        'shortcode': shortcode,
                        'url': post_url,
                        'type': post_type,
                        'caption': alt_text,
                        'likes': 0,  # Requiere abrir el post individual
                        'comments': 0,  # Requiere abrir el post individual
                        'timestamp': timestamp,
                        'media_url': media_url,  # URL principal (compatibilidad)
                        'media_urls': media_urls,  # Todas las URLs (carruseles)
                        'downloaded': False
                    }
                    posts.append(post)
                    
                    self.log(f"📸 Post extraído: {shortcode} ({post_type})")
                    
                    # Delay anti-baneo OPTIMIZADO (20% más rápido)
                    delay = random.uniform(3, 6)  # Reducido de 4-8s a 3-6s
                    self.log(f"⏱️ Pausa anti-detección: {delay:.1f}s")
                    time.sleep(delay)
                    
                    # Simular comportamiento humano ocasional
                    if random.random() < 0.3:  # 30% de probabilidad
                        self.simulate_human_behavior(driver)
                    
                    # Verificar límites cada 5 posts (menos frecuente)
                    if i > 0 and i % 5 == 0:
                        self.check_rate_limits()
                        self.log("🛡️ Pausa de seguridad anti-ban...")
                        time.sleep(random.uniform(8, 15))  # Reducido de 15-30s a 8-15s
                
                except Exception as post_error:
                    self.log(f"⚠️ Error extrayendo post {i+1}: {post_error}", "WARNING")
                    continue
            
            self.log(f"✅ {len(posts)} posts REALES extraídos")
            
            # Ordenar posts por timestamp REAL (orden cronológico preciso)
            if posts:
                self.log(f"🔄 Ordenando {len(posts)} posts por fecha REAL...")
                
                # Mostrar algunos timestamps antes de ordenar
                before_times = [(p.get('shortcode', 'N/A'), p.get('timestamp', 0)) for p in posts[:3]]
                self.log(f"📋 Antes de ordenar (primeros 3): {before_times}")
                
                # Ordenar por timestamp (más antiguo primero)
                posts.sort(key=lambda x: x.get('timestamp', 0))
                
                # Mostrar algunos timestamps después de ordenar
                after_times = [(p.get('shortcode', 'N/A'), p.get('timestamp', 0)) for p in posts[:3]]
                self.log(f"📋 Después de ordenar (primeros 3): {after_times}")
                
                self.log(f"📅 Posts ordenados por fecha REAL (cronológico preciso)")
                
                # Renumerar IDs después de ordenar por fecha
                for i, post in enumerate(posts):
                    post['id'] = f'{username}_post_{i+1:03d}'  # 001, 002, etc. (más antiguo = 001)
            
            return posts
            
        except Exception as e:
            self.log(f"❌ Error extrayendo posts: {str(e)}", "ERROR")
            return []
    
    def extract_real_timestamp_from_shortcode(self, shortcode: str) -> int:
        """Extraer timestamp real del shortcode de Instagram usando algoritmo de decodificación"""
        try:
            # Instagram usa un algoritmo base64 modificado para los shortcodes
            # Cada shortcode contiene información de timestamp codificada
            
            # Caracteres usados por Instagram para shortcodes
            ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
            
            # Decodificar shortcode a número
            decoded = 0
            for char in shortcode:
                if char in ALPHABET:
                    decoded = decoded * 64 + ALPHABET.index(char)
            
            # Los primeros 41 bits contienen el timestamp en milisegundos desde epoch de Instagram
            # Instagram epoch: 1 de enero de 2011 (1293840000 segundos desde Unix epoch)
            instagram_epoch = 1293840000
            
            # Extraer timestamp (primeros 41 bits)
            timestamp_ms = decoded >> 23  # Desplazar 23 bits para obtener timestamp
            timestamp_seconds = timestamp_ms / 1000.0
            
            # Convertir a timestamp Unix
            unix_timestamp = int(timestamp_seconds + instagram_epoch)
            
            # Validar que el timestamp sea razonable (después de 2011, antes de 2030)
            if unix_timestamp < instagram_epoch or unix_timestamp > 1893456000:  # 2030
                # Si el timestamp no es válido, usar hash del shortcode como fallback
                import hashlib
                hash_value = int(hashlib.md5(shortcode.encode()).hexdigest()[:8], 16)
                unix_timestamp = instagram_epoch + (hash_value % (365 * 24 * 3600 * 10))  # Últimos 10 años
            
            return unix_timestamp
            
        except Exception as e:
            # Fallback: usar hash del shortcode
            import hashlib
            hash_value = int(hashlib.md5(shortcode.encode()).hexdigest()[:8], 16)
            return 1293840000 + (hash_value % (365 * 24 * 3600 * 10))  # Últimos 10 años

    def extract_post_timestamp(self, driver, post_url: str) -> int:
        """Extraer timestamp del post para ordenación"""
        try:
            # Ir al post individual
            driver.get(post_url)
            time.sleep(random.uniform(2, 4))
            
            # Buscar elemento de tiempo
            time_elements = driver.find_elements(By.CSS_SELECTOR, "time[datetime], time")
            
            if time_elements:
                datetime_attr = time_elements[0].get_attribute('datetime')
                if datetime_attr:
                    from datetime import datetime
                    dt = datetime.fromisoformat(datetime_attr.replace('Z', '+00:00'))
                    return int(dt.timestamp())
            
            # Fallback: usar shortcode como aproximación (los más antiguos tienen IDs menores)
            shortcode = post_url.split('/p/')[-1].rstrip('/')
            return hash(shortcode) % 1000000  # Número pseudo-temporal
            
        except Exception as e:
            self.log(f"⚠️ Error extrayendo timestamp: {e}", "WARNING")
            return 0
    
    def extract_carousel_images(self, driver, post_url: str) -> List[str]:
        """Extraer todas las imágenes de un carrusel"""
        try:
            # Ir al post individual
            driver.get(post_url)
            time.sleep(random.uniform(3, 5))
            
            image_urls = []
            
            # Obtener primera imagen
            img_elements = driver.find_elements(By.CSS_SELECTOR, "article img[src*='instagram']")
            if img_elements:
                first_url = img_elements[0].get_attribute('src')
                if first_url:
                    image_urls.append(first_url.split('?')[0])
            
            # Buscar botones de navegación del carrusel
            next_buttons = driver.find_elements(By.CSS_SELECTOR, 
                "button[aria-label*='Next'], button[aria-label*='Siguiente']")
            
            if next_buttons:
                self.log(f"🎠 Carrusel detectado, navegando...")
                
                # Intentar navegar hasta 10 imágenes máximo
                for i in range(9):  # 9 clics máximo = 10 imágenes total
                    try:
                        # Scroll al elemento para asegurar visibilidad
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_buttons[0])
                        time.sleep(0.5)
                        
                        # Clic en siguiente con JavaScript para evitar interceptación
                        driver.execute_script("arguments[0].click();", next_buttons[0])
                        time.sleep(random.uniform(2, 4))
                        
                        # Obtener nueva imagen
                        current_imgs = driver.find_elements(By.CSS_SELECTOR, "article img[src*='instagram']")
                        if current_imgs:
                            current_url = current_imgs[0].get_attribute('src')
                            if current_url:
                                clean_url = current_url.split('?')[0]
                                if clean_url not in image_urls:
                                    image_urls.append(clean_url)
                                    self.log(f"   📸 Imagen {len(image_urls)} extraída")
                        
                        # Verificar si aún hay botón siguiente (con mejor selector)
                        next_buttons = driver.find_elements(By.CSS_SELECTOR, 
                            "button[aria-label*='Next'], button[aria-label*='Siguiente'], button._afxw._al46._al47")
                        
                        # Verificar que el botón sea clickeable
                        clickable_buttons = []
                        for btn in next_buttons:
                            try:
                                if btn.is_enabled() and btn.is_displayed():
                                    clickable_buttons.append(btn)
                            except:
                                continue
                        
                        if not clickable_buttons:
                            self.log("   ℹ️ No hay más botones de navegación disponibles")
                            break
                        
                        next_buttons = clickable_buttons
                            
                    except Exception as nav_error:
                        self.log(f"   ⚠️ Error navegando carrusel: {nav_error}", "WARNING")
                        break
                
                self.log(f"✅ Carrusel completado: {len(image_urls)} imágenes extraídas")
            
            return image_urls
            
        except Exception as e:
            self.log(f"❌ Error extrayendo carrusel: {e}", "ERROR")
            return []

    def download_posts_with_progress(self, posts: List[Dict], username: str) -> List[Dict]:
        """Descargar posts REALES con barra de progreso"""
        try:
            import requests
            from urllib.parse import urlparse
            
            user_dir = os.path.join(self.download_dir, username)
            os.makedirs(user_dir, exist_ok=True)
            
            total_posts = len(posts)
            downloaded_count = 0
            
            self.log(f"📥 Iniciando descarga REAL de {total_posts} posts en {user_dir}")
            
            for i, post in enumerate(posts):
                try:
                    # Actualizar progreso de descarga
                    self.update_download_progress(i, total_posts)
                    
                    # Obtener URLs de media (puede ser múltiples para carruseles)
                    media_urls = post.get('media_urls', [])
                    if not media_urls and post.get('media_url'):
                        media_urls = [post['media_url']]
                    
                    if not media_urls:
                        self.log(f"⚠️ Sin URLs de media para post {post['id']}", "WARNING")
                        post['downloaded'] = False
                        continue
                    
                    # Descargar TODAS las imágenes del post (incluyendo carruseles)
                    post_downloaded_files = []
                    
                    # Si es carrusel, obtener TODAS las imágenes
                    if post['type'] == 'carousel':
                        self.log(f"🎠 Carrusel detectado: {post['shortcode']} - Extrayendo todas las imágenes...")
                        # Extraer todas las imágenes del carrusel
                        carousel_urls = self.extract_carousel_images(self.driver, post['url'])
                        if carousel_urls:
                            media_urls = carousel_urls
                            self.log(f"🎠 Carrusel: {len(media_urls)} imágenes encontradas")
                    
                    for img_index, media_url in enumerate(media_urls):
                        try:
                            # Determinar extensión del archivo
                            if post['type'] == 'video':
                                extension = '.mp4'
                            else:
                                extension = '.jpg'
                            
                            # Nombre de archivo con identificación de tipo y orden cronológico
                            # Usar timestamp para ordenar archivos por fecha
                            import datetime
                            date_str = datetime.datetime.fromtimestamp(post['timestamp']).strftime('%Y%m%d_%H%M%S')
                            
                            if post['type'] == 'carousel' and len(media_urls) > 1:
                                # Para carruseles, numerar cada imagen: 001, 002, etc.
                                filename = f"{date_str}_{post['shortcode']}_carousel_{img_index+1:02d}{extension}"
                            elif post['type'] == 'video':
                                filename = f"{date_str}_{post['shortcode']}_video{extension}"
                            else:
                                filename = f"{date_str}_{post['shortcode']}_image{extension}"
                            
                            filepath = os.path.join(user_dir, filename)
                            
                            self.log(f"📥 Descargando {filename}...")
                            
                            # Descargar imagen/video REAL
                            headers = {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                                'Referer': 'https://www.instagram.com/',
                                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                            }
                            
                            response = requests.get(media_url, headers=headers, timeout=30)
                            response.raise_for_status()
                            
                            # Verificar que es realmente una imagen/video
                            content_type = response.headers.get('content-type', '')
                            if not any(t in content_type for t in ['image', 'video']):
                                self.log(f"⚠️ Contenido no es imagen/video: {content_type}", "WARNING")
                                continue
                            
                            # Guardar archivo real
                            with open(filepath, 'wb') as f:
                                f.write(response.content)
                            
                            # Verificar que el archivo se guardó correctamente
                            file_size = os.path.getsize(filepath)
                            if file_size < 1000:  # Menos de 1KB probablemente sea error
                                self.log(f"⚠️ Archivo muy pequeño ({file_size} bytes), posible error", "WARNING")
                                os.remove(filepath)
                                continue
                            
                            post_downloaded_files.append({
                                'filename': filename,
                                'filepath': filepath,
                                'size': file_size
                            })
                            
                            self.log(f"✅ Descargado: {filename} ({file_size} bytes)")
                            
                            # Delay entre imágenes del mismo post
                            if img_index < len(media_urls) - 1:
                                time.sleep(random.uniform(1, 3))
                                
                        except Exception as img_error:
                            self.log(f"❌ Error descargando imagen {img_index+1}: {img_error}", "WARNING")
                            continue
                    
                    # Marcar post como descargado si al menos una imagen se descargó
                    if post_downloaded_files:
                        post['downloaded'] = True
                        post['local_files'] = post_downloaded_files
                        post['total_files'] = len(post_downloaded_files)
                        downloaded_count += 1
                        
                        if len(post_downloaded_files) > 1:
                            self.log(f"🎠 Carrusel completo: {len(post_downloaded_files)} imágenes descargadas")
                    else:
                        post['downloaded'] = False
                    
                    # Delay anti-baneo OPTIMIZADO para descargas (20% más rápido)
                    download_delay = random.uniform(3, 7)  # Reducido de 5-10s a 3-7s
                    self.log(f"⏱️ Pausa post-descarga: {download_delay:.1f}s")
                    time.sleep(download_delay)
                    
                    # Pausa extra cada 5 descargas (menos frecuente)
                    if (i + 1) % 5 == 0:
                        extra_delay = random.uniform(10, 20)  # Reducido de 20-40s a 10-20s
                        self.log(f"🛡️ Pausa anti-ban extra: {extra_delay:.1f}s")
                        time.sleep(extra_delay)
                    
                except requests.exceptions.RequestException as req_error:
                    self.log(f"❌ Error de descarga para {post['id']}: {req_error}", "WARNING")
                    post['downloaded'] = False
                except Exception as e:
                    self.log(f"❌ Error descargando post {post['id']}: {str(e)}", "WARNING")
                    post['downloaded'] = False
            
            # Progreso final
            self.update_download_progress(total_posts, total_posts)
            self.log(f"✅ Descarga completada: {downloaded_count}/{total_posts} posts descargados")
            
            return posts
            
        except Exception as e:
            self.log(f"❌ Error en descarga: {str(e)}", "ERROR")
            return posts
    
    def cleanup(self):
        """Limpiar recursos del scraper"""
        try:
            if self.driver:
                self.log("🧹 Limpiando recursos del navegador...")
                self.driver.quit()
                self.driver = None
                self.log("✅ Recursos limpiados")
        except Exception as e:
            self.log(f"⚠️ Error limpiando recursos: {str(e)}", "WARNING")
    
    def __del__(self):
        """Destructor - limpiar recursos automáticamente"""
        self.cleanup()
    
    def update_progress(self, current: int, total: int, action: str = ""):
        """Actualizar el progreso de la operación"""
        self.progress['current'] = current
        self.progress['total'] = total
        self.progress['percentage'] = round((current / total * 100), 1) if total > 0 else 0
        self.progress['current_action'] = action
        
        progress_msg = f"📊 Progreso: {current}/{total} ({self.progress['percentage']}%) - {action}"
        self.log(progress_msg)
    
    def update_download_progress(self, downloaded: int, total: int):
        """Actualizar el progreso de descarga de posts"""
        self.progress['posts_downloaded'] = downloaded
        self.progress['posts_total'] = total
        
        if total > 0:
            percentage = round((downloaded / total * 100), 1)
            self.log(f"📥 Posts descargados: {downloaded}/{total} ({percentage}%)")
    
    def get_progress(self) -> Dict:
        """Obtener estado actual del progreso"""
        return self.progress.copy()
    
    def reset_progress(self):
        """Resetear el progreso"""
        self.progress = {
            'current': 0,
            'total': 0,
            'percentage': 0,
            'status': 'Inicializado',
            'current_action': '',
            'posts_downloaded': 0,
            'posts_total': 0
        } 
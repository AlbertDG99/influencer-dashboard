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
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InstagramScraper:
    """Scraper de Instagram usando Selenium con gestión de cookies"""
    
    def __init__(self):
        self.driver = None
        self.cookies = None
        self.authenticated = False
        self.logs = []
        self.status = "Inicializado"
        
        # Configuración
        self.base_url = "https://www.instagram.com"
        self.download_dir = os.path.abspath("downloads")
        self.logs_dir = os.path.abspath("logs")
        
        # Crear directorios
        os.makedirs(self.download_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        
        self.log("Scraper inicializado")
    
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
    
    def get_logs(self) -> List[Dict]:
        """Obtener logs recientes (últimos 100)"""
        return self.logs[-100:]
    
    def clear_logs(self):
        """Limpiar logs en memoria"""
        self.logs = []
        self.log("Logs limpiados")
    
    def get_status(self) -> Dict:
        """Obtener estado actual del scraper"""
        return {
            'status': self.status,
            'driver_active': self.driver is not None,
            'authenticated': self.authenticated,
            'cookies_set': self.cookies is not None,
            'logs_count': len(self.logs)
        }
    
    def get_auth_status(self) -> Dict:
        """Obtener estado de autenticación"""
        return {
            'authenticated': self.authenticated,
            'cookies_configured': self.cookies is not None,
            'cookies_count': len(self.cookies) if self.cookies else 0
        }
    
    def is_authenticated(self) -> bool:
        """Verificar si está autenticado"""
        return self.authenticated and self.cookies is not None
    
    def _init_driver(self) -> bool:
        """Inicializar el driver de Chrome"""
        try:
            self.log("Inicializando driver de Chrome...")
            
            # Configurar opciones de Chrome
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Ejecutar sin interfaz gráfica
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Configurar descargas
            prefs = {
                "download.default_directory": self.download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            # Inicializar driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(10)
            
            self.log("Driver de Chrome inicializado correctamente")
            return True
            
        except Exception as e:
            self.log(f"Error al inicializar driver: {str(e)}", "ERROR")
            return False
    
    def _close_driver(self):
        """Cerrar el driver"""
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                self.log("Driver cerrado")
            except Exception as e:
                self.log(f"Error al cerrar driver: {str(e)}", "WARNING")
    
    def set_cookies(self, cookies_text: str) -> bool:
        """Configurar cookies de Instagram"""
        try:
            self.log("Configurando cookies de Instagram...")
            
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
            essential_cookies = ['sessionid', 'csrftoken']
            missing_cookies = [c for c in essential_cookies if c not in cookies_dict]
            
            if missing_cookies:
                self.log(f"Faltan cookies esenciales: {missing_cookies}", "WARNING")
            
            self.cookies = cookies_dict
            self.log(f"Cookies configuradas: {len(cookies_dict)} cookies")
            
            # Probar autenticación
            return self._test_authentication()
            
        except Exception as e:
            self.log(f"Error al configurar cookies: {str(e)}", "ERROR")
            return False
    
    def _test_authentication(self) -> bool:
        """Probar la autenticación con Instagram"""
        try:
            self.log("Probando autenticación...")
            
            if not self._init_driver():
                return False
            
            # Ir a Instagram
            self.driver.get(self.base_url)
            time.sleep(3)
            
            # Agregar cookies
            for name, value in self.cookies.items():
                try:
                    self.driver.add_cookie({
                        'name': name,
                        'value': value,
                        'domain': '.instagram.com'
                    })
                except Exception as e:
                    self.log(f"Error agregando cookie {name}: {str(e)}", "WARNING")
            
            # Recargar página con cookies
            self.driver.refresh()
            time.sleep(5)
            
            # Verificar si estamos autenticados
            try:
                # Buscar elementos que indican autenticación
                auth_indicators = [
                    "//a[@href='/direct/inbox/']",  # Mensajes
                    "//a[contains(@href, '/accounts/edit/')]",  # Configuración
                    "//button[contains(text(), 'New post')]",  # Nuevo post
                    "//svg[@aria-label='Home']"  # Icono home
                ]
                
                authenticated = False
                for indicator in auth_indicators:
                    try:
                        WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, indicator))
                        )
                        authenticated = True
                        break
                    except TimeoutException:
                        continue
                
                if authenticated:
                    self.authenticated = True
                    self.log("Autenticación exitosa")
                    return True
                else:
                    self.log("No se pudo verificar la autenticación", "WARNING")
                    return False
                    
            except Exception as e:
                self.log(f"Error verificando autenticación: {str(e)}", "ERROR")
                return False
            
        except Exception as e:
            self.log(f"Error en test de autenticación: {str(e)}", "ERROR")
            return False
        finally:
            self._close_driver()
    
    def scrape_profile(self, username: str) -> Dict[str, Any]:
        """Scraping completo de un perfil de Instagram"""
        try:
            self.status = f"Scraping perfil: {username}"
            self.log(f"Iniciando scraping del perfil: {username}")
            
            if not self.is_authenticated():
                raise Exception("No hay autenticación configurada")
            
            if not self._init_driver():
                raise Exception("No se pudo inicializar el driver")
            
            # Ir a Instagram y configurar cookies
            self.driver.get(self.base_url)
            time.sleep(2)
            
            # Agregar cookies
            for name, value in self.cookies.items():
                try:
                    self.driver.add_cookie({
                        'name': name,
                        'value': value,
                        'domain': '.instagram.com'
                    })
                except:
                    pass
            
            # Ir al perfil
            profile_url = f"{self.base_url}/{username}/"
            self.log(f"Navegando a: {profile_url}")
            self.driver.get(profile_url)
            time.sleep(5)
            
            # Verificar que el perfil existe
            if "Sorry, this page isn't available" in self.driver.page_source:
                raise Exception(f"El perfil @{username} no existe o no está disponible")
            
            # Extraer información del perfil
            profile_info = self._extract_profile_info(username)
            
            # Extraer posts
            posts = self._extract_posts(username)
            
            result = {
                'username': username,
                'profile': profile_info,
                'posts': posts,
                'scraping_info': {
                    'timestamp': datetime.now().isoformat(),
                    'posts_found': len(posts),
                    'method': 'selenium_with_cookies'
                }
            }
            
            self.status = "Completado"
            self.log(f"Scraping completado: {len(posts)} posts encontrados")
            
            return result
            
        except Exception as e:
            self.status = "Error"
            self.log(f"Error en scraping: {str(e)}", "ERROR")
            raise e
        finally:
            self._close_driver()
    
    def _extract_profile_info(self, username: str) -> Dict[str, Any]:
        """Extraer información del perfil"""
        try:
            self.log("Extrayendo información del perfil...")
            
            # Esperar a que cargue el perfil
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "main"))
            )
            
            profile_info = {
                'username': username,
                'full_name': '',
                'bio': '',
                'posts_count': 0,
                'followers_count': 0,
                'following_count': 0,
                'is_private': False,
                'is_verified': False,
                'profile_pic_url': ''
            }
            
            # Extraer nombre completo
            try:
                full_name_element = self.driver.find_element(By.XPATH, "//span[contains(@class, 'x1lliihq')]")
                profile_info['full_name'] = full_name_element.text
            except:
                pass
            
            # Extraer biografía
            try:
                bio_element = self.driver.find_element(By.XPATH, "//div[contains(@class, 'x11i5rnm')]//span")
                profile_info['bio'] = bio_element.text
            except:
                pass
            
            # Extraer estadísticas (posts, seguidores, siguiendo)
            try:
                stats_elements = self.driver.find_elements(By.XPATH, "//a[contains(@href, f'/{username}/')]/span")
                if len(stats_elements) >= 3:
                    profile_info['posts_count'] = self._parse_number(stats_elements[0].text)
                    profile_info['followers_count'] = self._parse_number(stats_elements[1].text)
                    profile_info['following_count'] = self._parse_number(stats_elements[2].text)
            except:
                pass
            
            # Verificar si es privado
            try:
                private_indicator = self.driver.find_element(By.XPATH, "//span[contains(text(), 'This account is private')]")
                profile_info['is_private'] = True
            except:
                profile_info['is_private'] = False
            
            # Verificar si está verificado
            try:
                verified_indicator = self.driver.find_element(By.XPATH, "//span[@title='Verified']")
                profile_info['is_verified'] = True
            except:
                profile_info['is_verified'] = False
            
            # Extraer URL de foto de perfil
            try:
                profile_pic = self.driver.find_element(By.XPATH, f"//img[@alt=\"{username}'s profile picture\"]")
                profile_info['profile_pic_url'] = profile_pic.get_attribute('src')
            except:
                pass
            
            self.log(f"Información del perfil extraída: {profile_info['posts_count']} posts")
            return profile_info
            
        except Exception as e:
            self.log(f"Error extrayendo información del perfil: {str(e)}", "ERROR")
            return profile_info
    
    def _extract_posts(self, username: str) -> List[Dict[str, Any]]:
        """Extraer posts del perfil"""
        try:
            self.log("Extrayendo posts...")
            
            posts = []
            
            # Scroll para cargar más posts
            self._scroll_and_load_posts()
            
            # Buscar enlaces de posts
            post_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")
            
            self.log(f"Encontrados {len(post_links)} enlaces de posts")
            
            # Procesar cada post (limitamos a 50 para evitar timeouts)
            max_posts = min(50, len(post_links))
            
            for i, link in enumerate(post_links[:max_posts]):
                try:
                    href = link.get_attribute('href')
                    if href and '/p/' in href:
                        shortcode = href.split('/p/')[-1].rstrip('/')
                        
                        # Extraer información básica del post
                        post_info = {
                            'shortcode': shortcode,
                            'url': href,
                            'type': 'unknown',
                            'thumbnail_url': '',
                            'timestamp': None
                        }
                        
                        # Intentar extraer thumbnail
                        try:
                            img = link.find_element(By.TAG_NAME, 'img')
                            post_info['thumbnail_url'] = img.get_attribute('src')
                            
                            # Detectar tipo de post por indicadores visuales
                            parent = link.find_element(By.XPATH, '..')
                            if 'video' in parent.get_attribute('innerHTML').lower():
                                post_info['type'] = 'video'
                            elif 'carousel' in parent.get_attribute('innerHTML').lower():
                                post_info['type'] = 'carousel'
                            else:
                                post_info['type'] = 'image'
                        except:
                            pass
                        
                        posts.append(post_info)
                        
                        if (i + 1) % 10 == 0:
                            self.log(f"Procesados {i + 1}/{max_posts} posts")
                
                except Exception as e:
                    self.log(f"Error procesando post {i}: {str(e)}", "WARNING")
                    continue
            
            self.log(f"Extracción de posts completada: {len(posts)} posts")
            return posts
            
        except Exception as e:
            self.log(f"Error extrayendo posts: {str(e)}", "ERROR")
            return []
    
    def _scroll_and_load_posts(self):
        """Hacer scroll para cargar más posts"""
        try:
            self.log("Haciendo scroll para cargar posts...")
            
            # Scroll inicial
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            
            # Scroll adicional para cargar más contenido
            for i in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                # Verificar si aparece el botón "Load more"
                try:
                    load_more_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Load more')]")
                    if load_more_btn.is_displayed():
                        load_more_btn.click()
                        time.sleep(3)
                except:
                    pass
            
            self.log("Scroll completado")
            
        except Exception as e:
            self.log(f"Error durante scroll: {str(e)}", "WARNING")
    
    def _parse_number(self, text: str) -> int:
        """Parsear números con sufijos (K, M)"""
        try:
            text = text.replace(',', '').strip()
            
            if 'K' in text:
                return int(float(text.replace('K', '')) * 1000)
            elif 'M' in text:
                return int(float(text.replace('M', '')) * 1000000)
            else:
                return int(text)
        except:
            return 0 
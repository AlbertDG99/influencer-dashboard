#!/usr/bin/env python3
"""
Instagram Influencer Dashboard - Aplicación Simple
"""

import os
import json
import secrets
from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)

# Configuración segura
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

class InstagramScraper:
    def __init__(self):
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Configurar Chrome driver"""
        chrome_options = Options()
        if os.environ.get('CHROME_HEADLESS', 'True').lower() == 'true':
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(10)
        except Exception as e:
            print(f"Error configurando Chrome: {e}")
    
    def scrape_profile(self, username):
        """Scrapear perfil de Instagram"""
        try:
            url = f"https://www.instagram.com/{username}/"
            self.driver.get(url)
            time.sleep(3)
            
            # Obtener información básica
            profile_data = {
                'username': username,
                'followers': 'N/A',
                'following': 'N/A',
                'posts': 'N/A',
                'bio': 'N/A',
                'verified': False
            }
            
            # Intentar obtener followers
            try:
                followers_element = self.driver.find_element(By.XPATH, "//a[contains(@href, '/followers/')]/span")
                profile_data['followers'] = followers_element.get_attribute('title') or followers_element.text
            except:
                pass
            
            # Intentar obtener following
            try:
                following_element = self.driver.find_element(By.XPATH, "//a[contains(@href, '/following/')]/span")
                profile_data['following'] = following_element.get_attribute('title') or following_element.text
            except:
                pass
            
            # Intentar obtener posts
            try:
                posts_element = self.driver.find_element(By.XPATH, "//li[1]/span/span")
                profile_data['posts'] = posts_element.text
            except:
                pass
            
            # Intentar obtener bio
            try:
                bio_element = self.driver.find_element(By.XPATH, "//div[@data-testid='user-bio']")
                profile_data['bio'] = bio_element.text
            except:
                pass
            
            return profile_data
            
        except Exception as e:
            return {'error': str(e)}
    
    def close(self):
        """Cerrar driver"""
        if self.driver:
            self.driver.quit()

# Instancia global del scraper
scraper = None

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape_profile():
    """Endpoint para scrapear perfil"""
    global scraper
    
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        
        if not username:
            return jsonify({'error': 'Username requerido'}), 400
        
        # Inicializar scraper si no existe
        if not scraper:
            scraper = InstagramScraper()
        
        # Scrapear perfil
        result = scraper.scrape_profile(username)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Endpoint de salud"""
    return jsonify({'status': 'ok', 'message': 'Instagram Scraper funcionando'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Instagram Scraper iniciando en puerto {port}")
    print(f"🔧 Modo debug: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

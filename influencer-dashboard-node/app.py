#!/usr/bin/env python3
"""
Instagram Scraper - Aplicación web utilitaria con Flask y Selenium
"""

import os
import json
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from instagram_scraper import InstagramScraper
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Instancia global del scraper
scraper = InstagramScraper()

@app.route('/')
def index():
    """Página principal del scraper"""
    return render_template('index.html', 
                         auth_status=scraper.get_auth_status(),
                         scraper_status=scraper.get_status())

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    """Página de configuración de autenticación"""
    if request.method == 'POST':
        cookies_text = request.form.get('cookies', '').strip()
        
        if not cookies_text:
            return render_template('auth.html', 
                                 error="Por favor ingresa las cookies de Instagram")
        
        try:
            success = scraper.set_cookies(cookies_text)
            if success:
                session['auth_configured'] = True
                return redirect(url_for('index'))
            else:
                return render_template('auth.html', 
                                     error="Error al configurar las cookies")
        except Exception as e:
            return render_template('auth.html', 
                                 error=f"Error: {str(e)}")
    
    return render_template('auth.html', auth_status=scraper.get_auth_status())

@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    """Página de scraping"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        
        if not username:
            return render_template('scrape.html', 
                                 error="Por favor ingresa un nombre de usuario",
                                 auth_status=scraper.get_auth_status())
        
        # Verificar autenticación
        if not scraper.is_authenticated():
            return redirect(url_for('auth'))
        
        try:
            # Iniciar scraping
            result = scraper.scrape_profile(username)
            
            return render_template('results.html', 
                                 result=result,
                                 username=username,
                                 timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        except Exception as e:
            return render_template('scrape.html', 
                                 error=f"Error durante el scraping: {str(e)}",
                                 auth_status=scraper.get_auth_status())
    
    return render_template('scrape.html', auth_status=scraper.get_auth_status())

@app.route('/api/status')
def api_status():
    """API endpoint para obtener el estado del scraper"""
    return jsonify({
        'scraper_status': scraper.get_status(),
        'auth_status': scraper.get_auth_status(),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/scrape', methods=['POST'])
def api_scrape():
    """API endpoint para realizar scraping"""
    data = request.get_json()
    
    if not data or 'username' not in data:
        return jsonify({'error': 'Username requerido'}), 400
    
    username = data['username'].strip()
    
    if not username:
        return jsonify({'error': 'Username no puede estar vacío'}), 400
    
    if not scraper.is_authenticated():
        return jsonify({'error': 'Autenticación requerida'}), 401
    
    try:
        result = scraper.scrape_profile(username)
        return jsonify({
            'success': True,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/auth', methods=['POST'])
def api_auth():
    """API endpoint para configurar autenticación"""
    data = request.get_json()
    
    if not data or 'cookies' not in data:
        return jsonify({'error': 'Cookies requeridas'}), 400
    
    cookies_text = data['cookies'].strip()
    
    if not cookies_text:
        return jsonify({'error': 'Cookies no pueden estar vacías'}), 400
    
    try:
        success = scraper.set_cookies(cookies_text)
        
        if success:
            session['auth_configured'] = True
            return jsonify({
                'success': True,
                'message': 'Autenticación configurada correctamente',
                'auth_status': scraper.get_auth_status()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Error al configurar las cookies'
            }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/logs')
def logs():
    """Página de logs del scraper"""
    return render_template('logs.html', 
                         logs=scraper.get_logs(),
                         auth_status=scraper.get_auth_status())

@app.route('/clear_logs', methods=['POST'])
def clear_logs():
    """Limpiar logs del scraper"""
    scraper.clear_logs()
    return redirect(url_for('logs'))

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', 
                         error_code=404,
                         error_message="Página no encontrada"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', 
                         error_code=500,
                         error_message="Error interno del servidor"), 500

if __name__ == '__main__':
    # Crear directorios necesarios
    os.makedirs('downloads', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Configuración de desarrollo
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    
    print(f"🚀 Instagram Scraper iniciando en puerto {port}")
    print(f"📁 Directorio de descargas: {os.path.abspath('downloads')}")
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode) 
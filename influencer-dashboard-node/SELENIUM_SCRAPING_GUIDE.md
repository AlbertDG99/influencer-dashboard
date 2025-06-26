# 🔥 Instagram Selenium Scraping - Guía Completa

## 🎯 Objetivo

Este sistema implementa **scraping manual con Selenium** para engañar las medidas anti-scraping de Instagram y obtener **TODOS los posts** de un perfil, superando las limitaciones de 12 posts de los métodos tradicionales.

## 🚀 Características Principales

### ✨ Simulación de Navegador Real
- **Navegador Chrome real** con configuraciones anti-detección
- **Comportamiento humano simulado**: delays aleatorios, scroll natural, clics realistas
- **User-Agent realista** y headers de navegador auténtico
- **Sesión completa de navegador** con todas las cookies

### 🛡️ Medidas Anti-Detección
- Desactivación de indicadores de automatización (`webdriver`, `automation`)
- Scripts de ocultación de Selenium
- Delays humanos aleatorios (2-5 segundos)
- Patrones de scroll naturales
- Rotación de comportamientos

### 🔐 Autenticación Completa
- Uso de **todas las cookies del navegador**
- Sesión de Instagram completamente autenticada
- Verificación automática de estado de login
- Fallbacks robustos en caso de problemas de autenticación

## 📋 Requisitos del Sistema

### Dependencias Python
```bash
pip install selenium webdriver-manager beautifulsoup4
```

### Sistema Operativo
- **Linux**: Soporte completo (recomendado)
- **Windows**: Compatible
- **macOS**: Compatible

### Navegador
- **Google Chrome** (se instala automáticamente el driver)

## 🔧 Configuración

### 1. Obtener Cookies de Instagram

#### Método 1: Desde el Navegador
1. Abre Instagram en Chrome
2. Inicia sesión normalmente
3. Presiona `F12` para abrir DevTools
4. Ve a la pestaña `Application` > `Storage` > `Cookies` > `https://www.instagram.com`
5. Copia todas las cookies en formato: `name1=value1; name2=value2; ...`

#### Método 2: Usando la Consola del Navegador
```javascript
// Ejecutar en la consola de Instagram
document.cookie.split(';').map(c => c.trim()).join('; ')
```

### 2. Formato de Cookies Requerido
```
csrftoken=valor; mid=valor; dpr=valor; sessionid=valor; ds_user_id=valor; ig_did=valor; rur=valor; shbid=valor; shbts=valor
```

## 🌐 API Endpoints

### 1. Scraping Directo (POST)
```http
POST /api/v1/instagram/scrape-selenium/{username}
Content-Type: application/json

{
    "cookies": "csrftoken=...; sessionid=...; ds_user_id=..."
}
```

**Respuesta:**
```json
{
    "success": true,
    "method": "selenium_manual_scraping",
    "username": "albertodfg99",
    "profile": {
        "username": "albertodfg99",
        "full_name": "Alberto de la Fuente",
        "posts_count": 25,
        "followers_count": 127,
        "following_count": 150,
        "bio": "Bio del usuario...",
        "is_private": false,
        "is_verified": false
    },
    "posts": [
        {
            "shortcode": "ABC123",
            "url": "https://instagram.com/p/ABC123/media/?size=l",
            "type": "image",
            "post_url": "https://instagram.com/p/ABC123/"
        }
    ],
    "statistics": {
        "total_posts_in_profile": 25,
        "posts_scraped": 25,
        "posts_loaded_by_scroll": 25,
        "scraping_effectiveness": "25/25 posts"
    },
    "selenium_info": {
        "browser_used": "Chrome with human simulation",
        "authentication_status": true,
        "anti_detection_measures": [
            "Human-like delays (2-5 seconds)",
            "Random scroll patterns",
            "Realistic user agent",
            "Complete browser session simulation"
        ]
    }
}
```

### 2. Scraping con Streaming (GET)
```http
GET /api/v1/instagram/scrape-selenium-stream/{username}?cookies=...
```

**Respuesta (Server-Sent Events):**
```
data: {"type": "start", "message": "🚀 Iniciando scraping..."}
data: {"type": "info", "message": "🔧 Configurando navegador..."}
data: {"type": "profile", "data": {...}}
data: {"type": "posts", "data": [...]}
data: {"type": "complete", "message": "🎉 25 posts extraídos"}
```

## 💻 Uso Programático

### Python (Directo)
```python
from app.services.instagram_selenium_scraper import scrape_with_selenium

async def example():
    username = "albertodfg99"
    cookies = "csrftoken=...; sessionid=..."
    
    result = await scrape_with_selenium(username, cookies)
    
    if result.get('success'):
        posts = result.get('posts', [])
        print(f"Extraídos {len(posts)} posts")
    else:
        print(f"Error: {result.get('error')}")
```

### Python (Via API)
```python
import requests

def scrape_with_api():
    url = "http://localhost:8000/api/v1/instagram/scrape-selenium/albertodfg99"
    data = {"cookies": "csrftoken=...; sessionid=..."}
    
    response = requests.post(url, json=data, timeout=300)
    
    if response.status_code == 200:
        result = response.json()
        posts = result.get('posts', [])
        print(f"Extraídos {len(posts)} posts")
```

### JavaScript/Frontend
```javascript
async function scrapeWithSelenium(username, cookies) {
    const response = await fetch(`/api/v1/instagram/scrape-selenium/${username}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cookies })
    });
    
    const result = await response.json();
    
    if (result.success) {
        console.log(`Extraídos ${result.posts.length} posts`);
        return result.posts;
    } else {
        console.error('Error:', result.error);
    }
}
```

## 🔍 Proceso de Scraping Detallado

### 1. Inicialización del Navegador
- Configuración de Chrome con opciones anti-detección
- Instalación automática del ChromeDriver
- Aplicación de scripts de ocultación

### 2. Carga de Cookies
- Navegación inicial a Instagram
- Inyección de todas las cookies de autenticación
- Verificación de sesión activa

### 3. Navegación al Perfil
- Búsqueda del usuario (método humano)
- Navegación directa como fallback
- Verificación de carga correcta del perfil

### 4. Extracción de Información
- Datos del perfil (nombre, stats, bio)
- Detección de posts disponibles
- Identificación de contenido privado/verificado

### 5. Scroll Inteligente
- Scroll gradual para cargar más posts
- Detección de nuevos posts cargados
- Límite de seguridad para evitar loops infinitos
- Comportamiento humano (scroll hacia arriba ocasional)

### 6. Extracción de Posts
- Identificación de enlaces de posts
- Extracción de URLs de media
- Clasificación de tipo de contenido (imagen/video)
- Generación de shortcodes

## 📊 Comparación de Métodos

| Método | Posts Máximos | Autenticación | Detección | Velocidad |
|--------|---------------|---------------|-----------|-----------|
| **Público** | ~12 posts | No | Alta | Rápida |
| **API Autenticada** | ~12 posts | Básica | Alta | Rápida |
| **Selenium Manual** | **TODOS** | Completa | **Muy Baja** | Lenta |

## ⚡ Optimizaciones y Configuraciones

### Delays Configurables
```python
human_delays = {
    'page_load': (3, 7),      # Espera después de cargar página
    'scroll': (1, 3),         # Entre scrolls
    'click': (0.5, 2),        # Después de clics
    'typing': (0.1, 0.3),     # Entre caracteres
    'between_actions': (2, 5)  # Entre acciones principales
}
```

### Límites de Seguridad
- **Max scrolls**: 50 intentos
- **Timeout**: 300 segundos (5 minutos)
- **No new posts limit**: 5 intentos consecutivos sin nuevos posts

### Configuración de Chrome
```python
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
```

## 🛠️ Troubleshooting

### Problemas Comunes

#### 1. Error de ChromeDriver
```bash
# Solución: Reinstalar webdriver-manager
pip uninstall webdriver-manager
pip install webdriver-manager
```

#### 2. Timeout del Navegador
```python
# Aumentar timeout
response = requests.post(url, json=data, timeout=600)  # 10 minutos
```

#### 3. Cookies Inválidas
- Verificar que las cookies sean recientes (< 24 horas)
- Asegurar que incluyan `sessionid`, `csrftoken`, `ds_user_id`
- Verificar formato correcto (separadas por `;`)

#### 4. Perfil No Encontrado
- Verificar que el username sea correcto
- Verificar que el perfil sea público o tengas acceso
- Probar con otro perfil conocido

### Logs de Debug
```python
import logging
logging.getLogger('selenium').setLevel(logging.DEBUG)
```

## 🚨 Consideraciones Legales y Éticas

### ⚠️ Uso Responsable
- **Solo para perfiles públicos** o con permiso explícito
- **Respetar términos de servicio** de Instagram
- **No hacer scraping masivo** o comercial
- **Usar delays apropiados** para no sobrecargar servidores

### 🔒 Privacidad
- **No almacenar cookies** de otros usuarios
- **No compartir datos personales** extraídos
- **Usar solo para propósitos legítimos**

### 📝 Términos de Instagram
- Instagram prohíbe el scraping automatizado
- Este método es para **investigación y desarrollo**
- **Usar bajo tu propia responsabilidad**

## 🎯 Casos de Uso Recomendados

### ✅ Usos Apropiados
- **Análisis de tu propio perfil**
- **Investigación académica** (con permisos)
- **Backup personal** de contenido
- **Desarrollo y testing** de aplicaciones

### ❌ Usos Inapropiados
- Scraping masivo comercial
- Violación de privacidad
- Spam o automatización maliciosa
- Reventa de datos extraídos

## 📈 Resultados Esperados

### Perfiles Públicos
- **Éxito esperado**: 80-95% de posts
- **Limitaciones**: Instagram puede seguir bloqueando algunos posts
- **Efectividad**: Significativamente mejor que métodos API

### Perfiles Privados
- **Requiere**: Seguir al usuario y tener acceso
- **Éxito esperado**: Similar a públicos si tienes acceso
- **Limitaciones**: Sin acceso = 0 posts

## 🔄 Actualizaciones y Mantenimiento

### Actualizaciones de Instagram
- Instagram actualiza regularmente sus medidas anti-scraping
- Este sistema se actualiza para mantener compatibilidad
- Reportar problemas en el repositorio

### Monitoreo de Efectividad
- Logs detallados de cada scraping
- Estadísticas de éxito/fallo
- Métricas de posts extraídos vs. disponibles

---

## 🎉 Conclusión

El **sistema de scraping con Selenium** representa la evolución natural para superar las limitaciones de Instagram. Aunque es más lento que los métodos API, proporciona acceso a **significativamente más contenido** al simular un navegador real.

**¡Úsalo responsablemente y disfruta del acceso completo a los datos de Instagram!** 🚀 
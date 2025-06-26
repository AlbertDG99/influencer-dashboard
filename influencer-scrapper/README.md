# 🚀 Instagram Scraper - README

## 📋 **Índice**
1. [Descripción General](#descripción-general)
2. [Configuración y Setup](#configuración-y-setup)
3. [Funcionalidades](#funcionalidades)
4. [Seguridad Anti-Ban](#seguridad-anti-ban)
5. [Uso y Operación](#uso-y-operación)
6. [Optimizaciones](#optimizaciones)
7. [Solución de Problemas](#solución-de-problemas)
8. [Estructura del Proyecto](#estructura-del-proyecto)

---

## 🎯 **Descripción General**

**Instagram Scraper** es una herramienta avanzada de web scraping diseñada específicamente para extraer contenido de Instagram de manera segura y eficiente. Utiliza Selenium con medidas anti-detección robustas para evitar baneos.

### ✨ **Características Principales**
- 🎠 **Carruseles Completos**: Descarga TODAS las imágenes de carruseles
- 📅 **Ordenación Cronológica**: Archivos ordenados por fecha real usando timestamps
- 🛡️ **Anti-Detección Avanzada**: Configuración fija, delays aleatorios, comportamiento humano
- ⚡ **Optimizado**: Tiempos reducidos 20% manteniendo seguridad
- 🌐 **Interface Web**: Dashboard utilitarian para monitoreo
- 📊 **Progreso en Tiempo Real**: Barras de progreso y logs detallados

---

## 🔧 **Configuración y Setup**

### 📋 **Requisitos**
- Python 3.8+
- Chrome/Chromium browser
- ChromeDriver en PATH del sistema
- Conexión a internet estable

### 🚀 **Instalación**
```bash
# 1. Clonar/descargar proyecto
cd influencer-scrapper

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate.fish  # Para fish shell
# source venv/bin/activate     # Para bash/zsh

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar aplicación
python app.py
```

### 🔐 **Configuración de Cookies**
Las cookies están **pre-configuradas** con cuenta activa:
- **User ID**: 75438268055
- **Session ID**: 75438268055%3AGCjZNv%3A28%3AAYeQZUg
- **CSRF Token**: MikM2znlBoVNnlGFva2AYpAGW2eJF2CV

---

## 🎯 **Funcionalidades**

### 📸 **Extracción de Posts**
- **Detección Automática**: Identifica posts simples, carruseles y videos
- **Scroll Inteligente**: Carga TODOS los posts del perfil (hasta 25)
- **Timestamps Reales**: Decodifica shortcodes para obtener fechas exactas
- **Metadatos**: Extrae información de perfil (seguidores, verificación, etc.)

### 🎠 **Carruseles Avanzados**
- **Navegación Automática**: Detecta y navega por todas las imágenes
- **Clic Inteligente**: Usa JavaScript para evitar interceptaciones
- **Verificación**: Confirma que botones sean clickeables
- **Nomenclatura**: `fecha_shortcode_carousel_01.jpg`, `_02.jpg`, etc.

### 📥 **Descarga de Medios**
- **Archivos Reales**: Descarga JPG/MP4 reales, no simulaciones
- **Verificación**: Confirma tipo de contenido y tamaño mínimo
- **Organización**: Estructura de carpetas por usuario
- **Progreso**: Tracking en tiempo real de descargas

### 📂 **Estructura de Archivos**
```
downloads/username/
├── 20231201_120000_ABC123_image.jpg          # Post más antiguo
├── 20231202_140000_DEF456_carousel_01.jpg    # Carrusel 1/3
├── 20231202_140000_DEF456_carousel_02.jpg    # Carrusel 2/3
├── 20231202_140000_DEF456_carousel_03.jpg    # Carrusel 3/3
├── 20231203_160000_GHI789_video.mp4          # Video
└── 20231204_180000_JKL012_image.jpg          # Post más reciente
```

---

## 🛡️ **Seguridad Anti-Ban**

### 🔒 **Configuración Fija (Enfoque Realista)**
- **User Agent**: Chrome 120.0.0.0 Windows (fijo por sesión)
- **Resolución**: 1920x1080 (consistente)
- **Idioma**: en-US (no cambia)
- **Plataforma**: Win32 (estable)

**Rationale**: Los usuarios reales no cambian de dispositivo cada pocos segundos.

### ⏱️ **Delays Optimizados**
- **Navegación**: 3-6 segundos entre posts
- **Descargas**: 3-7 segundos por imagen
- **Scroll**: 4-6 segundos entre páginas
- **Pausas de seguridad**: 8-15 segundos cada 5 operaciones
- **Comportamiento humano**: 1.5-3.5 segundos ocasional

### 🤖 **Simulación de Comportamiento**
- **Scroll gradual**: Movimiento natural en 3 etapas
- **Mouse aleatorio**: Simulación de movimientos
- **Eventos de navegador**: Dispatch de eventos scroll
- **Pausas variables**: Nunca patrones fijos

### 📊 **Rate Limiting**
- **Navegación**: Máximo 12 posts/minuto
- **Descargas**: Máximo 10 imágenes/minuto
- **Requests totales**: Máximo 15/minuto
- **Verificación**: Cada 5 operaciones

---

## 🎮 **Uso y Operación**

### 🌐 **Interface Web**
- **Dashboard**: `http://localhost:5000`
- **Scraping**: `http://localhost:5000/scrape`
- **Logs**: `http://localhost:5000/logs`
- **API**: `http://localhost:5000/api/status`

### 📊 **Proceso de Scraping**
1. **Configurar navegador** (2-3 segundos)
2. **Cargar cookies** (3-5 segundos)
3. **Navegar a perfil** (5-8 segundos)
4. **Extraer información** (10-15 segundos)
5. **Scroll y cargar posts** (2-5 minutos)
6. **Descargar medios** (5-15 minutos)

### 🕐 **Tiempos Estimados**
- **15 posts simples**: 13-20 minutos
- **25 posts con carruseles**: 15-25 minutos
- **Perfil completo promedio**: 12-18 minutos

### 🌅 **Horarios Recomendados**
- **Óptimos**: 6:00-9:00 y 22:00-2:00
- **Aceptables**: 14:00-17:00
- **Evitar**: 9:00-12:00 y 18:00-21:00

---

## ⚡ **Optimizaciones**

### 🎯 **Mejoras Implementadas**
- **ChromeDriverManager eliminado**: Uso directo del sistema
- **Tiempos reducidos 20%**: Balance velocidad/seguridad
- **Scroll mejorado**: 15 intentos, carga gradual
- **Carruseles completos**: Todas las imágenes extraídas
- **Ordenación real**: Timestamps decodificados de shortcodes

### 📈 **Rendimiento**
- **Antes**: 20-30 minutos (15 posts)
- **Después**: 13-20 minutos (15 posts)
- **Mejora**: 25-35% más rápido

### 🔍 **Algoritmo de Timestamp**
```python
# Decodifica shortcode de Instagram para obtener fecha real
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
decoded = sum(ALPHABET.index(char) * (64 ** i) for i, char in enumerate(reversed(shortcode)))
timestamp_ms = decoded >> 23  # Primeros 41 bits
unix_timestamp = timestamp_ms / 1000.0 + 1293840000  # Instagram epoch
```

---

## 🚨 **Solución de Problemas**

### ❌ **Errores Comunes**

#### 1. **ChromeDriver no encontrado**
```bash
# Instalar ChromeDriver
sudo apt install chromium-chromedriver  # Ubuntu/Debian
brew install chromedriver              # macOS
```

#### 2. **Carruseles no funcionan**
- ✅ **Solucionado**: Clic con JavaScript
- ✅ **Scroll automático**: Elemento visible antes de clic
- ✅ **Verificación**: Botones clickeables

#### 3. **Archivos corruptos**
- ✅ **Verificación**: Content-type y tamaño mínimo
- ✅ **Headers reales**: Referer de Instagram
- ✅ **Timeout**: 30 segundos por descarga

#### 4. **Detección/Baneo**
- **Síntomas**: Captchas, errores 429, contenido no carga
- **Solución**: Pausar 1-2 horas, cambiar IP, reducir velocidad

### 🔍 **Debugging**
```bash
# Ver logs en tiempo real
tail -f logs/scraper_$(date +%Y%m%d).log

# Verificar estado API
curl http://localhost:5000/api/status

# Verificar archivos descargados
ls -la downloads/username/
file downloads/username/*.jpg  # Verificar que sean imágenes reales
```

---

## 📁 **Estructura del Proyecto**

```
influencer-scrapper/
├── app.py                      # Aplicación Flask principal
├── instagram_scraper.py        # Lógica de scraping
├── requirements.txt            # Dependencias
├── README_COMPLETO.md         # Esta documentación
├── templates/                  # Plantillas HTML
│   ├── base.html
│   ├── index.html
│   ├── scrape.html
│   ├── results.html
│   └── logs.html
├── downloads/                  # Archivos descargados
├── logs/                      # Logs del sistema
├── venv/                      # Entorno virtual
└── start.sh                   # Script de inicio
```

---

## 🚀 **Límites y Recomendaciones**

### 📊 **Límites Diarios**
- **Conservador**: 2-3 perfiles/día
- **Moderado**: 5-7 perfiles/día  
- **Máximo**: 10 perfiles/día (con pausas largas)

### 🔄 **Rotación**
- **Entre perfiles**: 30-60 minutos
- **Entre sesiones**: 2-4 horas
- **Cambio de IP**: Cada 20-30 perfiles

### ⚠️ **Señales de Alerta**
- **Captchas**: Parar inmediatamente
- **Errores 429**: Pausa de 5 minutos
- **Contenido no carga**: Reducir velocidad
- **Bloqueos**: Cambiar IP/sesión

---

## 🔮 **Desarrollo Futuro**

### 🎯 **Mejoras Planificadas**
- **Proxies rotativos**: Mayor anonimato
- **Cache inteligente**: Evitar re-descargas
- **Metadatos avanzados**: Likes, comentarios, captions
- **Recuperación**: Reanudar descargas interrumpidas
- **Paralelización**: Múltiples perfiles simultáneos

### 📈 **Métricas de Éxito**
- **Tasa de éxito**: >95% de descargas exitosas
- **Tiempo promedio**: <20 minutos por perfil
- **Detección**: <1% de baneos temporales
- **Calidad**: 100% archivos reales verificados

---

**✅ PROYECTO COMPLETO Y OPTIMIZADO**

*Versión: 2.0 - Optimizada y Documentada*  
*Última actualización: Diciembre 2024* 
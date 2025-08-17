# 🔍 Instagram Scraper Simple

Aplicación web simple para analizar perfiles de Instagram usando Python Flask y Selenium.

## ✨ Características

- 🔍 **Scraping de Instagram** con Selenium
- 📊 **Análisis de métricas** básicas (seguidores, posts, bio)
- 🎯 **Interfaz web simple** y responsive
- 🚀 **Una sola aplicación** Python
- 💻 **Sin dependencias complejas**

## 🏗️ Arquitectura

```
instagram-scraper/
├── 📄 app.py              # Aplicación principal Flask
├── 📁 templates/          # Template HTML
│   └── index.html        # Página principal
├── 📄 requirements.txt    # Dependencias Python
├── 📄 package.json        # Scripts de npm
└── 📄 .env.example       # Variables de entorno
```

## 🚀 Quick Start

### 1. Instalar dependencias
```bash
npm run install:python
# o
pip install -r requirements.txt
```

### 2. Configurar variables de entorno
```bash
cp env.example .env
# Edita .env con tus valores
```

### 3. Ejecutar aplicación
```bash
npm run dev
# o
python app.py
```

### 4. Abrir en navegador
```
http://localhost:5000
```

## 🔧 Configuración

### Variables de Entorno

```bash
# Seguridad
SECRET_KEY=your-secret-key-here

# Configuración de la aplicación
FLASK_DEBUG=False
PORT=5000

# Configuración de Chrome
CHROME_HEADLESS=True
```

### Dependencias Python

- **Flask**: Framework web
- **Selenium**: Automatización del navegador
- **webdriver-manager**: Gestión automática del Chrome driver

## 📱 Uso

### Scraping de Instagram

1. **Abrir la aplicación** en tu navegador
2. **Ingresar username** de Instagram (sin @)
3. **Hacer clic en "Analizar Perfil"**
4. **Ver resultados** en tiempo real

### Métricas Obtenidas

- 👥 **Seguidores**: Número de seguidores
- 👤 **Siguiendo**: Número de cuentas que sigue
- 📸 **Posts**: Número de publicaciones
- 📝 **Bio**: Descripción del perfil
- ✅ **Verificado**: Si la cuenta está verificada

## 🚨 Limitaciones

- **Sin autenticación**: Solo perfiles públicos
- **Rate limiting**: Instagram puede bloquear requests excesivos
- **Cambios de UI**: Instagram cambia su interfaz frecuentemente

## 🔒 Seguridad

- ✅ Variables de entorno para credenciales
- ✅ Clave secreta generada automáticamente
- ✅ Modo debug deshabilitado por defecto

## 🐛 Troubleshooting

### Error: Chrome driver no encontrado
```bash
pip install webdriver-manager
```

### Error: Selenium no funciona
```bash
pip install selenium
```

### Error: Flask no funciona
```bash
pip install flask
```

## 📞 Soporte

- **Issues**: GitHub Issues
- **Documentación**: Este README

---

⭐ **Si te gusta este proyecto, dale una estrella en GitHub!**

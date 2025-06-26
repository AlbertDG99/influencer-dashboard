#!/bin/bash

# 🚀 Instagram Scraper - Script de Inicio
# Versión: 2.0 Optimizada

echo "🚀 Iniciando Instagram Scraper..."

# Verificar que estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo "❌ Error: Ejecutar desde el directorio influencer-scrapper"
    exit 1
fi

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar/actualizar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt --quiet

# Crear directorios necesarios
mkdir -p downloads logs

# Verificar ChromeDriver
if ! command -v chromedriver &> /dev/null; then
    echo "⚠️  Advertencia: ChromeDriver no encontrado en PATH"
    echo "   Instalar con: sudo apt install chromium-chromedriver"
fi

# Mostrar información
echo ""
echo "✅ Configuración completada"
echo "🌐 Servidor: http://localhost:5000"
echo "📊 Dashboard: http://localhost:5000"
echo "🔌 API: http://localhost:5000/api/status"
echo ""
echo "🛡️  Medidas anti-ban ACTIVAS"
echo "⚡ Tiempos optimizados (-20%)"
echo "🎠 Carruseles completos"
echo "📅 Ordenación cronológica"
echo ""

# Ejecutar aplicación
echo "🚀 Iniciando servidor..."
python app.py 
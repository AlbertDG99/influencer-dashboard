# 🚀 Instagram Dashboard - Proyectos Separados

Este repositorio contiene dos proyectos independientes para scraping de Instagram, cada uno con su propio enfoque y tecnologías.

## 📁 Estructura de Proyectos

### 🔧 [`influencer-scrapper/`](./influencer-scrapper/) - Proyecto Python Puro
**Aplicación web utilitaria con Flask y Selenium**

- **Tecnología**: Python + Flask + Selenium
- **Enfoque**: Scraping real con descarga de archivos
- **Características**:
  - ✅ Barra de progreso en tiempo real
  - ✅ Descarga automática de posts
  - ✅ Medidas anti-detección realistas
  - ✅ Interfaz web utilitaria
  - ✅ API REST completa
  - ✅ Logs en tiempo real

### 🎯 [`influencer-dashboard-node/`](./influencer-dashboard-node/) - Proyecto Full-Stack
**Dashboard completo con backend Python y frontend React/Next.js**

- **Tecnología**: Python (Backend) + React/Next.js (Frontend)
- **Enfoque**: Dashboard completo para análisis de influencers
- **Características**:
  - ✅ Backend API con FastAPI/Flask
  - ✅ Frontend moderno con React
  - ✅ Base de datos para almacenamiento
  - ✅ Análisis avanzado de datos
  - ✅ Docker para deployment

## 🎯 ¿Cuál Proyecto Usar?

### Usa `influencer-scrapper` si:
- ✅ Quieres una herramienta **simple y directa**
- ✅ Necesitas **descargar posts** a tu computadora
- ✅ Prefieres una **interfaz utilitaria** sin complicaciones
- ✅ Quieres **ver progreso en tiempo real**
- ✅ Solo necesitas **Python** (sin Node.js)

### Usa `influencer-dashboard-node` si:
- ✅ Quieres un **dashboard completo**
- ✅ Necesitas **análisis avanzado** de datos
- ✅ Prefieres una **interfaz moderna** con React
- ✅ Quieres **almacenar datos** en base de datos
- ✅ Planeas **escalar** la aplicación

## 🚀 Inicio Rápido

### Para `influencer-scrapper`:
```bash
cd influencer-scrapper
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
**Accede a**: http://localhost:5000

### Para `influencer-dashboard-node`:
```bash
cd influencer-dashboard-node
# Backend
pip install -r requirements.txt
python app.py

# Frontend (en otra terminal)
cd frontend
npm install
npm run dev
```
**Accede a**: http://localhost:3000

## 📊 Comparación de Proyectos

| Característica | influencer-scrapper | influencer-dashboard-node |
|---|---|---|
| **Complejidad** | 🟢 Simple | 🟡 Avanzado |
| **Tecnologías** | Python + Flask | Python + React |
| **Tiempo de setup** | 🟢 5 minutos | 🟡 15 minutos |
| **Descarga de archivos** | ✅ Sí | ❌ No |
| **Progreso visual** | ✅ Tiempo real | ✅ Dashboard |
| **Base de datos** | ❌ No | ✅ Sí |
| **API REST** | ✅ Básica | ✅ Completa |
| **Interfaz** | 🔧 Utilitaria | 🎨 Moderna |
| **Docker** | ❌ No | ✅ Sí |

## 🛡️ Medidas Anti-Detección

Ambos proyectos implementan:
- ✅ **Configuración consistente** (más realista)
- ✅ **Delays inteligentes** entre acciones
- ✅ **Comportamiento humano** simulado
- ✅ **Límites conservadores** de velocidad
- ✅ **Gestión de cookies** avanzada

## 📝 Documentación

### influencer-scrapper
- [README.md](./influencer-scrapper/README.md) - Guía completa
- [CHANGELOG.md](./influencer-scrapper/CHANGELOG.md) - Historial de cambios
- [ENFOQUE_REALISTA.md](./influencer-scrapper/ENFOQUE_REALISTA.md) - Filosofía anti-detección

### influencer-dashboard-node
- [README.md](./influencer-dashboard-node/README.md) - Guía de instalación
- [AUTHENTICATION_SUMMARY.md](./influencer-dashboard-node/AUTHENTICATION_SUMMARY.md) - Autenticación
- [INTEGRATION_COMPLETE.md](./influencer-dashboard-node/INTEGRATION_COMPLETE.md) - Integración

## 🤝 Contribuir

Cada proyecto tiene su propio sistema de contribución:

1. **Fork** el repositorio
2. **Elige** el proyecto (`influencer-scrapper` o `influencer-dashboard-node`)
3. **Crea** una rama para tu feature
4. **Desarrolla** en el directorio correspondiente
5. **Envía** un Pull Request

## 📄 Licencia

MIT License - Ver [LICENSE](./LICENSE) para más detalles.

## 🆘 Soporte

- **Issues**: Usa el sistema de issues de GitHub
- **Especifica** qué proyecto estás usando
- **Incluye** logs y detalles del error

---

**🎯 Resumen**: Dos proyectos independientes para diferentes necesidades - uno simple y directo, otro completo y escalable.
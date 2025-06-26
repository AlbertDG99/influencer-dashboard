# 🚀 Inicio Rápido - Influencer Dashboard Node

## ⚡ Instalación en 15 Minutos

### 1. Preparar Backend (Python)
```bash
cd influencer-dashboard-node
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Preparar Frontend (Node.js)
```bash
cd frontend
npm install
```

### 3. Iniciar Backend
```bash
# En terminal 1
cd influencer-dashboard-node
source venv/bin/activate
python app.py
```

### 4. Iniciar Frontend
```bash
# En terminal 2
cd influencer-dashboard-node/frontend
npm run dev
```

### 5. Abrir en navegador
```
Frontend: http://localhost:3000
Backend API: http://localhost:5000
```

## 🎯 Primer Uso

### 1. Configurar Autenticación
1. Ve a la sección de **Configuración**
2. Ingresa las cookies de Instagram
3. Verifica la conexión

### 2. Explorar Dashboard
1. **Dashboard Principal** - Estadísticas generales
2. **Análisis de Influencers** - Métricas detalladas
3. **Scraping Avanzado** - Herramientas de extracción
4. **Base de Datos** - Historial de datos

### 3. Realizar Análisis
1. Ingresa username del influencer
2. Inicia análisis completo
3. Ve resultados en dashboard
4. Exporta datos si necesario

## 🔧 Características Principales

- ✅ **Dashboard moderno** - Interfaz React profesional
- ✅ **Base de datos** - Almacenamiento persistente
- ✅ **Análisis avanzado** - Métricas y estadísticas
- ✅ **API completa** - Backend robusto
- ✅ **Docker ready** - Deployment fácil

## 🛠️ Comandos Útiles

```bash
# Backend en puerto diferente
PORT=5001 python app.py

# Frontend en puerto diferente
PORT=3001 npm run dev

# Build para producción
npm run build

# Docker (si está configurado)
docker-compose up -d

# Ver logs del backend
tail -f logs/*.log
```

## 🐳 Docker (Opcional)

```bash
# Construir y ejecutar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar servicios
docker-compose down
```

## 🗄️ Base de Datos

### Configuración
- Por defecto usa SQLite
- Para producción: PostgreSQL/MySQL
- Configurar en `config.env`

### Migraciones
```bash
# Crear tablas
python -c "from app import create_tables; create_tables()"

# Backup
cp database.db database_backup.db
```

## 🆘 Problemas Comunes

### Puertos ocupados
```bash
# Backend
PORT=5001 python app.py

# Frontend
PORT=3001 npm run dev
```

### Error de Node.js
```bash
# Verificar versión
node --version  # Requiere 16+
npm --version

# Limpiar cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Error de dependencias Python
```bash
# Reinstalar entorno
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📊 Estructura del Proyecto

```
influencer-dashboard-node/
├── app.py                  # Backend Flask/FastAPI
├── requirements.txt        # Dependencias Python
├── config.env             # Variables de entorno
├── frontend/              # Aplicación React
│   ├── src/
│   ├── package.json
│   └── next.config.js
├── backend/               # API Backend
├── database/              # Modelos y migraciones
└── docker-compose.yml     # Configuración Docker
```

## 🔗 API Endpoints

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/dashboard` | GET | Datos del dashboard |
| `/api/influencer/:id` | GET | Datos de influencer |
| `/api/scrape` | POST | Iniciar scraping |
| `/api/analytics` | GET | Métricas y análisis |
| `/api/export` | GET | Exportar datos |

¡Listo! Ya tienes el dashboard completo funcionando con React y base de datos. 🎉 
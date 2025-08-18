# Influfinder – Instagram Influencer Finder

Proyecto completo para explorar y analizar influencers de Instagram por categoría, hashtags e idioma. Incluye API REST (Flask), frontend HTML/CSS minimalista y guía de despliegue en Vercel.

## Características

- API RESTful con documentación OpenAPI/Swagger
- Arquitectura modular (Repositorios, Servicios, Controladores)
- Configuración centralizada via variables de entorno
- Logging estructurado (JSON)
- Manejo robusto de errores
- CORS y cabeceras de seguridad (CSP, HSTS, etc.)
- Health check y métricas Prometheus
- Exportación de resultados a CSV/XLSX
- Tests unitarios con pytest
- Frontend responsive con modo oscuro/claro

## Estructura de carpetas

```
Influfinder/
  backend/
    api/
      docs/
        swagger.py
    app.py
    wsgi.py
    config.py
    extensions.py
    logging_config.py
    web/
      controllers/
        influencer_controller.py
        export_controller.py
        health_controller.py
      errors.py
    domain/
      models/
        influencer.py
      repositories/
        base.py
      services/
        influencer_service.py
        export_service.py
        instagram_api_service.py
        scraping_service.py
    infrastructure/
      repositories/
        memory_influencer_repository.py
        instagram_influencer_repository.py
        factory.py
      scraping/
        instagram_scraper.py
      external/
        instagram_client.py
    utils/
      security.py
      pagination.py
      validators.py
    tests/
      conftest.py
      test_api.py
      test_influencer_service.py
  frontend/
    index.html
    styles/
      main.css
    js/
      app.js
  scripts/
    dev.ps1
    dev.sh
    test.ps1
    test.sh
  requirements.txt
  .env.example
  vercel.json
```

## Requisitos

- Python 3.10+
- pip

## Instalación (Windows PowerShell)

```powershell
cd Influfinder
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:FLASK_APP = "backend/app.py"
$env:FLASK_ENV = "development"
$env:PYTHONPATH = "."
python backend/app.py
```

La API estará en `http://127.0.0.1:5000`. La documentación Swagger en `http://127.0.0.1:5000/api/docs`.

Frontend está servido por Flask en `/`.

## Variables de entorno

Ver `.env.example` y config en `backend/config.py`.

- `FLASK_ENV`: development|production
- `SECRET_KEY`: clave secreta de Flask
- `CORS_ORIGINS`: orígenes permitidos, separados por comas
- `LOG_LEVEL`: DEBUG|INFO|WARNING|ERROR
- `ENABLE_SECURITY_HEADERS`: true|false
- `INSTAGRAM_ACCESS_TOKEN`: token de acceso de Instagram Graph API
- `IG_BUSINESS_ACCOUNT_ID`: ID del usuario de Instagram Business/Creator
- `GRAPH_API_VERSION`: versión, por defecto `v19.0`
- `USE_INSTAGRAM_API`: true/false para activar el repositorio oficial (si no, usa datos de memoria)

## Despliegue en Vercel

`vercel.json` ya está configurado para enrutar API y frontend a `backend/app.py`.

Pasos:

```bash
npm i -g vercel
vercel login
vercel
```

En Vercel, configura las variables de entorno anteriores en Project → Settings → Environment Variables.

## Tests

```bash
pytest -q
```

## Nota sobre Instagram API / Scraping

Para uso real, configura `INSTAGRAM_ACCESS_TOKEN` y `IG_BUSINESS_ACCOUNT_ID` en entorno local/Vercel. Los endpoints de hashtag (búsqueda, top/recent media) y Business Discovery están implementados en `instagram_api_service.py`. Si no configuras credenciales, el proyecto usa un repositorio en memoria con datos de ejemplo.

## Licencia

MIT

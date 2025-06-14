# Influencer Dashboard

Aplicación para analizar perfiles de influencers para campañas de marketing.

## Stack Tecnológico

Este proyecto utiliza una arquitectura de microservicios con un backend en Python y un frontend en Next.js.

### Backend

*   **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
*   **Servidor ASGI**: [Uvicorn](https://www.uvicorn.org/)
*   **Base de Datos**: [PostgreSQL](https://www.postgresql.org/) `v13`
*   **ORM**: [SQLModel](https://sqlmodel.tiangolo.com/)
*   **Tareas Asíncronas**: [Celery](https://docs.celeryq.dev/en/stable/)
*   **Broker de Mensajes**: [Redis](https://redis.io/) `v6.2-alpine`
*   **Autenticación**: `passlib[bcrypt]` y `python-jose[cryptography]`
*   **Inteligencia Artificial**:
    *   [PyTorch](https://pytorch.org/)
    *   [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)
    *   [OpenAI CLIP](https://github.com/openai/CLIP)

### Frontend

*   **Framework**: [Next.js](https://nextjs.org/) `v15.3.3`
*   **Librería UI**: [React](https://react.dev/) `v19.0.0`
*   **Lenguaje**: [TypeScript](https://www.typescriptlang.org/) `v5`
*   **Estilos**: [Tailwind CSS](https://tailwindcss.com/) `v4`

## Funcionalidades Principales

*   **Análisis de Influencers**: El sistema permite analizar perfiles de influencers utilizando modelos de IA para extraer información relevante.
*   **Procesamiento Asíncrono**: Las tareas de análisis que consumen mucho tiempo se ejecutan en segundo plano utilizando Celery para no bloquear la interfaz de usuario.
*   **Gestión de usuarios**: Sistema de autenticación para la gestión de usuarios.
*   **API RESTful**: Un API construida con FastAPI para comunicar el frontend con los servicios del backend.

## Instalación y Puesta en Marcha

Para lanzar el proyecto, necesitarás tener instalado [Docker](https://www.docker.com/) y [Docker Compose](https://docs.docker.com/compose/). El frontend requiere [Node.js](https://nodejs.org/en).

### 1. Levantar los servicios del Backend

La base de datos, el servidor de backend y el worker de Celery se gestionan con Docker Compose.

Antes de iniciarlos, copia `backend/.env.example` a `backend/.env` y ajusta las URL de conexión según tu entorno.

```bash
docker-compose up -d --build
```

Esto levantará los siguientes servicios:
*   `backend`: El servidor de FastAPI en `http://localhost:8000`
*   `db`: La base de datos PostgreSQL en `localhost:5434`
*   `redis`: El broker de Redis en `localhost:6379`
*   `worker`: El worker de Celery para tareas asíncronas.

### 2. Lanzar el Frontend

El frontend se debe ejecutar de forma local en un entorno de Node.js.

```bash
cd frontend
npm install
npm run dev
```

La aplicación frontend estará disponible en `http://localhost:3000`.

### Requisitos de Hardware

Para el análisis con los modelos de IA, el `docker-compose.yml` está configurado para hacer uso de GPUs de NVIDIA (`driver: nvidia`). Si no dispones de una GPU, deberás comentar o eliminar la sección `deploy` del servicio `worker` en el fichero `docker-compose.yml`.

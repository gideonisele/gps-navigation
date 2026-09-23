# GPS Navigation Platform

A full-stack GPS navigation platform built with:

- PostgreSQL
- PostGIS
- FastAPI
- SQLAlchemy
- GeoAlchemy2
- Alembic
- Next.js
- React
- TypeScript
- MapLibre GL JS
- Docker Compose

## Current Build

Levels 0-3 implement the initial vertical slice:

Browser / MapLibre
→ Next.js
→ FastAPI
→ SQLAlchemy / GeoAlchemy2
→ PostgreSQL / PostGIS

Users can select geographic locations on the map and persist latitude,
longitude, and PostGIS geography points through the API.

## Services

- Frontend: Next.js / MapLibre
- Backend: FastAPI
- Database: PostgreSQL / PostGIS

## Development

Start the application:

    docker compose up -d

Check containers:

    docker compose ps

Stop the application:

    docker compose down

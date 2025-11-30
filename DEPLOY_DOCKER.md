# Deploy Locally with Docker Compose

This document explains how to run the full stack (Postgres, Django backend, React frontend) locally using Docker Compose.

Prerequisites
- Docker and Docker Compose installed
- Project code checked out (root contains `docker-compose.yml`)

Steps
1. Copy the .env template and edit:

```powershell
cd "C:\Users\manve\Desktop\Student tracking"
cp .env.docker .env.docker.local
# edit .env.docker.local to set SECRET_KEY and email/db passwords
notepad .env.docker.local
```

2. Build and start services:

```powershell
# from project root
docker compose up --build
```

3. The services will be available at:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

Notes
- The first run will run migrations and collectstatic automatically via `entrypoint.sh` in the backend image.
- Media files uploaded by users are stored in `backend/media` on the host (mounted into the container).
- The PostgreSQL data is persisted in a Docker named volume `db_data`.

Stopping and removing containers

```powershell
# stop
docker compose down

# stop and remove volumes
docker compose down -v
```

Troubleshooting
- If migrations fail, check backend logs:
  - `docker compose logs backend`
- If frontend cannot reach backend, ensure `CORS_ALLOWED_ORIGINS` includes `http://localhost:3000` and `VITE_API_BASE_URL` is set accordingly in `student-frontend/.env` when building outside docker.

Production notes
- For production, prefer separate build steps and a managed Postgres instance (like Render Postgres or AWS RDS). Adjust `ALLOWED_HOSTS`, `DEBUG=False`, and secure secrets.

# Simple Task Manager

## Build and run the application

**1. Setup environment**

Copy templates and adjust values:
```sh
cp .env.example .env
cp compose.override.yaml.example compose.override.yaml
```

**2. Build and init database**

```sh
docker compose build
docker compose run backend uv run manage.py migrate
```

**3. Run**

```sh
docker compose up
```

**Web-UI:**
By default, the Web UI will be available at http://localhost:8000.

**API (Swagger):**
API Documentaion is available at http://localhost:8000/docs.

## Development

- Backend: see `backend/README.md` for more information
- Frontend: see `frontend/README.md` for more information

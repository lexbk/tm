# Simple Task Manager

## Build and run the application

**1. Setup environment**

Create local environment variables from templates:

```sh
cp .env.example .env
```

```sh
cp compose.override.yaml.example compose.override.yaml
```

**2. Build and init database**

Build:
```sh
docker compose build
```

Run migrations:
```sh
docker compose run backend uv run manage.py migrate
```

**3. Run**

Create external docker network:
```sh
docker network create tm-net
```

Run application:
```sh
docker compose up
```

**Users:**
By default, the following default users will be created for testing purposes:
- `admin` with password `admin` (Django Admin)
- `user1` with password `123` (User to log in Task Manager)
- `user2` with password `123` (User to log in Task Manager)

**Web-UI:**
By default, the Web UI will be available at http://localhost:8000.

**API (Swagger):**
API Documentaion is available at http://localhost:8000/docs.

## Development

- Backend: see `backend/README.md` for more information
- Frontend: see `frontend/README.md` for more information

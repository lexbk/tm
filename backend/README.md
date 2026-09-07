# Task Manger Backend

The backend application for managing tasks. It provides a RESTful API for creating, updating, deleting, and retrieving tasks.

This is part of the Task Manager project, which is web-application for managing tasks. See `../readme.md` for more details.

## Development

**1. Set up environment**

```sh
uv sync --all-groups
```

Run migrations and start dev server:

```sh
uv run manage.py migrate
uv run manage.py runserver
```

**2. Tests commands:**

```sh
# Run tests
uv run pytest --cov-report html --cov=.

# Lints
uv run ruff check
uv run mypy .
```

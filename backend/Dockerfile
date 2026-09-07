# =======================================================
# STAGE 1: Install system and python libraries to a prefix
# =======================================================
ARG DOCKER_PYTHON_IMAGE

FROM ${DOCKER_PYTHON_IMAGE} AS backend-builder
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    less \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up the python virtual environment using UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin/:$PATH"
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1

# Copy project config and install dependencies
COPY pyproject.toml ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --all-groups


# =======================================================
# STAGE 2: Final lean runtime image
# =======================================================
FROM ${DOCKER_PYTHON_IMAGE} AS backend-runtime

# Copy ALL system changes from builder stage
COPY --from=backend-builder / /

WORKDIR /app

# Copy backend application code
COPY app app
COPY config config
COPY core core
COPY manage.py manage.py
COPY static static

ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
ENV UV_OFFLINE=1
ENV PATH="/root/.local/bin/:$PATH"

EXPOSE 8001
CMD ["uv", "run", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8001"]

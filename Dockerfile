# --- BASE STAGE ---
FROM python:3.13-slim-trixie AS base

# --- BUILDER STAGE ---
FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim AS builder

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# --- PRODUCTION STAGE ---
FROM base AS production

ARG PORT=$PORT

COPY --from=builder --chown=app:app /app /app

# Place executables in the environment at the front of the path
ENV HOME=/app/src PATH="/app/.venv/bin:$PATH"

WORKDIR /app/src

COPY --chmod=755 <<EOT /entrypoint.sh
#!/usr/bin/env bash
set -xe
python manage.py migrate --noinput &
granian --interface wsgi --blocking-threads 3 config.wsgi:application --host 0.0.0.0 --port $PORT
EOT

ENTRYPOINT ["/entrypoint.sh"]

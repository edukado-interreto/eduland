##### BASE STAGE #####
FROM python:3.14-alpine AS base

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1 \
    UV_PROJECT_ENVIRONMENT=$VIRTUAL_ENV

##### BUILDER STAGE #####
FROM ghcr.io/astral-sh/uv:python3.14-alpine AS builder

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1 UV_PYTHON_DOWNLOADS=0

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Use a different virtual environment from /app/.venv
ENV UV_PROJECT_ENVIRONMENT=/opt/venv

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Then, add the rest of the project source code and install it
COPY pyproject.toml uv.lock /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

##### DEVELOPMENT STAGE #####
FROM base AS development

ENV PYTHONDONTWRITEBYTECODE=1

COPY --from=builder --chown=appuser:appuser $VIRTUAL_ENV $VIRTUAL_ENV

RUN \
--mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
--mount=type=cache,target=/root/.cache/uv \
--mount=type=bind,source=uv.lock,target=uv.lock \
--mount=type=bind,source=pyproject.toml,target=pyproject.toml \
uv sync --frozen

WORKDIR /app/src

##### PRODUCTION STAGE #####
FROM base AS production

ENV HOME="/app/src"

COPY --from=builder --chown=appuser:appuser $VIRTUAL_ENV $VIRTUAL_ENV
COPY --chown=appuser:appuser ./src /app/src

WORKDIR /app/src

RUN python manage.py collectstatic -v 2 --noinput
RUN ls -la /app/staticfiles/

COPY --chmod=755 <<EOT /entrypoint.sh
#!/usr/bin/env bash
set -xe
python manage.py migrate --noinput &
granian config.wsgi:application
EOT

ENTRYPOINT ["/entrypoint.sh"]

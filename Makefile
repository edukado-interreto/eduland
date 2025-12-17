dc := docker compose
django := uv run python manage.py

all: run

install:
	mkdir -p uploads
	mkdir -p .docker/postgres_data .docker/caddy_data
	cp .env.example .env
	$(dc) build

certs:
	openssl req -x509 -newkey ed25519 -days 3650 -noenc -keyout etc/eduland.key -out etc/eduland.cert -subj "/CN=eduland.localhost" -addext "subjectAltName=DNS:eduland.localhost,DNS:*.eduland.localhost,IP:127.0.0.1"

run:
	$(dc) up --build django

runserver:
	$(django) runserver

shell:
	$(dc) exec django ./manage.py shell_plus

migrations:
	$(dc) exec django ./manage.py makemigrations

migrate:
	$(dc) exec django ./manage.py migrate

lint:
	uv run ruff format --check src/apps src/config
	uv run ruff check src/apps src/config
	uv run basedpyright src/apps src/config

beercss:
	$(eval TAG=$(shell xhs api.github.com/repos/beercss/beercss/tags | jq -r '.[0].name' | cut -c 2-))
	wget -O src/public/static/beer-$(TAG).min.js https://cdn.jsdelivr.net/npm/beercss@$(TAG)/dist/cdn/beer.min.js
	wget -O src/public/static/beer-$(TAG).min.css https://cdn.jsdelivr.net/npm/beercss@$(TAG)/dist/cdn/beer.min.css

vue:
	npm --prefix ui run build-only

vue-dev:
	npm --prefix ui run dev

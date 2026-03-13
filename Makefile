dc := docker compose
django := uv run python manage.py

all: run

install:
	mkdir -p uploads
	mkdir -p .docker/postgresql .docker/caddy/data
	cp .env.example .env
	cp config/.env.example config/.env
	$(dc) build

run:
	$(dc) up --build django

run-vite:
	$(dc) -f compose.yaml -f compose-vite.yaml up proxy django vue

runserver:
	$(django) runserver

shell:
	$(dc) exec django ./manage.py shell_plus

urls:
	$(dc) exec django ./manage.py show_urls

superuser:
	$(dc) exec django ./manage.py createsuperuser

migrations:
	$(dc) exec django ./manage.py makemigrations

migrate:
	$(dc) exec django ./manage.py migrate

lint:
	uv run ruff format --check apps config
	uv run ruff check --select I apps config
	uv run ruff check apps config

isort:
	uv run ruff check --select I --fix apps config

beercss:
	$(eval TAG=$(shell xhs api.github.com/repos/beercss/beercss/tags | jq -r '.[0].name' | cut -c 2-))
	wget -r -np -nH -l1 --cut-dirs=4 --reject 'index.html' -P public/static/beercss-$(TAG) https://cdn.jsdelivr.net/npm/beercss@$(TAG)/dist/cdn/

vue:
	npm --prefix ui run build-only

vue-dev:
	npm --prefix ui run dev

django := uv run python manage.py

all: run

run:
	docker compose up --build django

runserver:
	$(django) runserver

lint:
	uv run ruff format --check apps config
	uv run ruff check apps config
	uv run basedpyright apps config

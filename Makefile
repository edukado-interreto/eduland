django := uv run python manage.py

all: runserver

runserver:
	$(django) runserver

lint:
	uv run ruff format --check apps config
	uv run ruff check apps config
	uv run basedpyright apps config

django := uv run python src/manage.py
run := npm run --prefix ui

all: runserver

runserver:
	$(django) runserver

lint:
	uv run ruff format --check src
	uv run ruff check src
	uv run basedpyright src

css:
	$(run)

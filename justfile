dc := "docker compose"
dc_exec := dc + " exec django"
django := dc_exec + " ./manage.py"

default:
    @just --list

install: create_secrets apply_selinux copy_dotenv copy_django_dotenv build
    mkdir -p uploads containers/db/postgresql containers/caddy/data
    @printf "\nFarite. Nun tajpu:\n\njust run\n"

# Start the Django project in dev mode
run:
    {{ dc }} up --build django

# Start the Django project with the Vite dev server
run-vite:
    {{ dc }} -f compose.yaml -f compose-vite.yaml up proxy django vue

# Start Django locally, outside of Docker
[working-directory('src')]
runserver:
    uv run python manage.py runserver

build:
    {{ dc }} build django

[group('django')]
superuser:
    {{ django }} createsuperuser

[group('django')]
migrations args='':
    {{ django }} makemigrations {{ args }}

[group('django')]
migrate args='':
    {{ django }} migrate {{ args }}

[group('django')]
sh:
    {{ dc_exec }} ash

[group('django')]
shell:
    {{ django }} shell_plus

[group('django')]
dbshell:
    {{ dc }} exec postgres psql -U eduland eduland

[group('django')]
urls:
    {{ django }} show_urls

# Run the tests with coverage, against the PostgreSQL of Docker Compose
[group('django')]
test args='':
    {{ dc_exec }} pytest {{ args }}

[group('uv')]
uv-sync:
    uv sync --locked

[group('uv')]
update:
    uv lock --upgrade

[group('uv')]
format:
    uv run ruff format src

[group('uv')]
lint:
    uv run ruff format --check src
    uv run ruff check --select I src
    uv run ruff check src

[group('uv')]
isort:
    uv run ruff check --select I --fix src

[group('vue')]
vue:
    npm -C ui run build-only

[group('vue')]
vue-dev:
    npm -C ui run dev

# Download the latest BeerCSS release into the static files
beercss:
    #!/usr/bin/env sh
    TAG=$(xhs api.github.com/repos/beercss/beercss/tags | jq -r '.[0].name' | cut -c 2-)
    wget -r -np -nH -l1 --cut-dirs=4 --reject 'index.html' -P src/config/static/beercss-$TAG https://cdn.jsdelivr.net/npm/beercss@$TAG/dist/cdn/

copy_dotenv:
    #!/usr/bin/env python3
    from os import getegid, geteuid
    from pathlib import Path

    dotenv = Path(".env")
    if dotenv.exists():
        print(f"Dosiero {dotenv} jam ekzistas, ne estos kreite.")
        exit(0)

    REPLACEMENTS = {
        "USER_ID = 1000": f"USER_ID = {geteuid()}",
        "GROUP_ID = 1000": f"GROUP_ID = {getegid()}",
    }

    with open(".env.example") as envfile_ex, open(dotenv, "w") as envfile:
        for line in envfile_ex:
            for key, value in REPLACEMENTS.items():
                line = line.replace(key, value)
            envfile.write(line)

copy_django_dotenv:
    #!/usr/bin/env python3
    from pathlib import Path
    from secrets import token_urlsafe

    django_env = Path("src/config/.env")
    if django_env.exists():
        print(f"Dosiero {django_env} jam ekzistas, ne estos kreite.")
        exit(0)

    REPLACEMENTS = {"EDULAND_SECRET_KEY = \n": f"EDULAND_SECRET_KEY = {token_urlsafe(40)}\n"}

    with open("src/config/.env.example") as dj_ex, open(django_env, "w") as dj:
        for line in dj_ex:
            for key, value in REPLACEMENTS.items():
                line = line.replace(key, value)
            dj.write(line)

create_secrets:
    #!/usr/bin/env python3
    from pathlib import Path
    from secrets import token_urlsafe

    SECRETS_DIR = Path("containers/secrets")
    SECRETS_FILES = ["postgres-password"]

    SECRETS_DIR.mkdir(parents=True, exist_ok=True)
    for secret_file in (SECRETS_DIR / name for name in SECRETS_FILES):
        # Ne tuŝi se ekzistas kaj plenas
        if secret_file.exists():
            with open(secret_file) as f:
                if len(f.read()) > 1:
                    print(f"Dosiero {secret_file} jam ekzistas.")
                    continue
        with open(secret_file, "w") as s:
            s.write(token_urlsafe(40))
            print(f"Pasvorto skribite en {secret_file}")

apply_selinux:
    -command -v chcon >/dev/null 2>&1 && exec chcon -t container_file_t -R containers/secrets

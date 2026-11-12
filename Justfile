ruff := "uv run ruff"
mypy := "uv run mypy"
pytest := "uv run pytest"
pre_commit := "uv run pre-commit"
compose := "docker compose"
compose_test := "docker compose -p raydahub-test -f docker-compose.yaml -f compose/test.yaml"
test_db_env := "POSTGRES_HOST=localhost POSTGRES_PORT=15432 POSTGRES_USER=test POSTGRES_PASSWORD=test POSTGRES_DB=test"

[private]
default:
    @just --list

[group('ruff')]
lint:
    {{ ruff }} check .

[group('ruff')]
lint-fix:
    {{ ruff }} check --fix .

[group('ruff')]
format:
    {{ ruff }} format .

[group('ruff')]
format-check:
    {{ ruff }} format --check --diff .

[group('mypy')]
typecheck:
    {{ mypy }}

[group('pytest')]
test *args:
    {{ pytest }} {{ args }}

[group('pytest')]
test-cov:
    {{ pytest }} --cov

[group('pytest')]
test-infra *args:
    {{ pytest }} --infra {{ args }}

[group('quality')]
check: lint format-check typecheck

[group('quality')]
check-ci: check test-cov
    SKIP=ruff-check,ruff-format,mypy {{ pre_commit }} run --all-files --show-diff-on-failure

[group('quality')]
fix: lint-fix format

[group('docker')]
gen-secrets:
    python3 scripts/gen_secrets.py

[group('docker')]
build:
    docker build -t raydahub:latest .

[group('docker')]
up:
    {{ compose }} up -d

[group('docker')]
up-local:
    {{ compose }} -f docker-compose.yaml -f compose/local.yaml up -d

[group('docker')]
up-db:
    {{ compose }} up -d postgres

[group('docker')]
up-test:
    {{ compose_test }} up -d

[group('docker')]
up-test-db:
    {{ compose_test }} up -d postgres

[group('docker')]
down:
    {{ compose }} down

[group('alembic')]
migrate:
    {{ compose }} run --rm migrate

[group('alembic')]
migration message:
    {{ test_db_env }} {{ compose_test }} up -d --wait postgres
    {{ test_db_env }} uv run alembic upgrade head
    {{ test_db_env }} uv run alembic revision --autogenerate -m "{{ message }}"

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

[group('code')]
code-lint:
    {{ ruff }} check .

[group('code')]
code-lint-fix:
    {{ ruff }} check --fix .

[group('code')]
code-format:
    {{ ruff }} format .

[group('code')]
code-format-check:
    {{ ruff }} format --check --diff .

[group('code')]
code-typecheck:
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

[group('code')]
code-check: code-lint code-format-check code-typecheck

[group('quality')]
check-ci: code-check test-cov
    SKIP=ruff-check,ruff-format,mypy {{ pre_commit }} run --all-files --show-diff-on-failure

[group('code')]
code-fix: code-lint-fix code-format

[group('docker')]
gen-secrets:
    python3 scripts/gen_secrets.py

[group('docker')]
docker-build:
    docker build -t raydahub:latest .

[group('docker')]
docker-up:
    {{ compose }} up -d

[group('docker')]
docker-up-local:
    {{ compose }} -f docker-compose.yaml -f compose/local.yaml up -d

[group('docker')]
docker-up-db:
    {{ compose }} up -d postgres

[group('docker')]
docker-up-test:
    {{ compose_test }} up -d

[group('docker')]
docker-up-test-db:
    {{ compose_test }} up -d postgres

[group('docker')]
docker-down:
    {{ compose }} down

[group('alembic')]
migrate:
    {{ compose }} run --rm migrate

[group('alembic')]
migration message:
    {{ test_db_env }} {{ compose_test }} up -d --wait postgres
    {{ test_db_env }} uv run alembic upgrade head
    {{ test_db_env }} uv run alembic revision --autogenerate -m "{{ message }}"

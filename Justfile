ruff := "uv run ruff"
mypy := "uv run mypy"
pre_commit := "uv run pre-commit"
compose := "docker compose"

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

[group('quality')]
check: lint format-check typecheck

[group('quality')]
check-ci: check
    SKIP=ruff-check,ruff-format,mypy {{ pre_commit }} run --all-files --show-diff-on-failure

[group('quality')]
fix: lint-fix format

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
down:
    {{ compose }} down

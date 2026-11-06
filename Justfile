ruff := "uv run ruff"
mypy := "uv run mypy"
pre_commit := "uv run pre-commit"

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

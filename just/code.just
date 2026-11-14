ruff := "uv run ruff"
mypy := "uv run mypy"

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

[group('code')]
code-check: code-lint code-format-check code-typecheck

[group('code')]
code-fix: code-lint-fix code-format

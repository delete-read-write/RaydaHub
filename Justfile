import 'just/code.just'
import 'just/pytest.just'
import 'just/docker.just'
import 'just/alembic.just'

pre_commit := "uv run pre-commit"
compose := "docker compose"
compose_test := "docker compose -p raydahub-test -f docker-compose.yaml -f compose/test.yaml"

[private]
default:
    @just --list

[group('quality')]
check-ci: code-check
    SKIP=ruff-check,ruff-format,mypy {{ pre_commit }} run --all-files --show-diff-on-failure

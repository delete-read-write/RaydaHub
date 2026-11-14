test_db_env := "POSTGRES_HOST=localhost POSTGRES_PORT=15432 POSTGRES_USER=test POSTGRES_PASSWORD=test POSTGRES_DB=test"

[group('alembic')]
migrate:
    {{ compose }} run --rm migrate

[group('alembic')]
migration message:
    {{ test_db_env }} {{ compose_test }} up -d --wait postgres
    {{ test_db_env }} uv run alembic upgrade head
    {{ test_db_env }} uv run alembic revision --autogenerate -m "{{ message }}"

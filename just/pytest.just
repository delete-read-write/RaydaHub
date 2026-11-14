pytest := "uv run pytest"

[group('pytest')]
test *args:
    {{ pytest }} {{ args }}

[group('pytest')]
test-cov:
    {{ pytest }} --cov

[group('pytest')]
test-infra *args:
    {{ pytest }} --infra {{ args }}

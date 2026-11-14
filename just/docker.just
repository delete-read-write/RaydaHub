[group('docker')]
gen-secrets:
    mkdir -p secrets
    [ -f secrets/postgres_password ] || python3 -c 'import secrets; print(secrets.token_urlsafe(32), end="")' > secrets/postgres_password
    chmod 755 secrets
    chmod 644 secrets/postgres_password

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

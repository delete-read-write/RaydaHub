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

import secrets
from pathlib import Path
from typing import Final

SECRETS_DIR: Final[Path] = Path("secrets")
POSTGRES_PASSWORD: Final[Path] = SECRETS_DIR / "postgres_password"


def main() -> None:
    SECRETS_DIR.mkdir(exist_ok=True)

    if not POSTGRES_PASSWORD.exists():
        POSTGRES_PASSWORD.write_text(secrets.token_urlsafe(32))

    SECRETS_DIR.chmod(0o755)
    POSTGRES_PASSWORD.chmod(0o644)


if __name__ == "__main__":
    main()

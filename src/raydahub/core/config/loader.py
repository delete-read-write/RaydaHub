from typing import TYPE_CHECKING

from raydahub.core.config.env import (
    AppEnvSettings,
    BaseEnvSettings,
    FastAPIEnvSettings,
    LoggingEnvSettings,
    PostgresEnvSettings,
    SQLAEnvSettings,
)

if TYPE_CHECKING:
    from raydahub.core.config.settings import (
        AppSettings,
        FastAPISettings,
        LoggingSettings,
        PostgresSettings,
        SQLASettings,
    )


def _load_env[E: BaseEnvSettings](env_cls: type[E]) -> E:
    return env_cls()


def load_app_settings() -> AppSettings:
    return _load_env(AppEnvSettings)


def load_logging_settings() -> LoggingSettings:
    return _load_env(LoggingEnvSettings)


def load_fastapi_settings() -> FastAPISettings:
    return _load_env(FastAPIEnvSettings)


def load_sqla_settings() -> SQLASettings:
    return _load_env(SQLAEnvSettings)


def load_postgres_settings() -> PostgresSettings:
    return _load_env(PostgresEnvSettings)

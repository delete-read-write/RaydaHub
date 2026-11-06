from typing import TYPE_CHECKING

from raydahub.core.config.env import AppEnvSettings, BaseEnvSettings, LoggingEnvSettings

if TYPE_CHECKING:
    from raydahub.core.config.settings import AppSettings, LoggingSettings


def _load_env[E: BaseEnvSettings](env_cls: type[E]) -> E:
    return env_cls()


def load_app_settings() -> AppSettings:
    return _load_env(AppEnvSettings)


def load_logging_settings() -> LoggingSettings:
    return _load_env(LoggingEnvSettings)

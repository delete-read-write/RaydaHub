from pydantic_settings import BaseSettings, SettingsConfigDict

from raydahub.core.config.settings import AppSettings, FastAPISettings, LoggingSettings


class BaseEnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class AppEnvSettings(BaseEnvSettings, AppSettings):
    model_config = SettingsConfigDict(env_prefix="APP_")


class LoggingEnvSettings(BaseEnvSettings, LoggingSettings):
    model_config = SettingsConfigDict(env_prefix="LOGGING_")


class FastAPIEnvSettings(BaseEnvSettings, FastAPISettings):
    model_config = SettingsConfigDict(env_prefix="FASTAPI_")

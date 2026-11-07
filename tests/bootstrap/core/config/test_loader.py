import pytest

from raydahub.core.config.loader import (
    load_app_settings,
    load_fastapi_settings,
    load_logging_settings,
)


def test_load_app_settings_reads_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_SERVICE_NAME", "test-service")
    monkeypatch.setenv("APP_SERVICE_VERSION", "test-version")

    sut = load_app_settings()

    assert sut.service_name == "test-service"
    assert sut.service_version == "test-version"


@pytest.mark.parametrize("logging_level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
def test_load_logging_settings_reads_env_vars(
    monkeypatch: pytest.MonkeyPatch,
    logging_level: str,
) -> None:
    monkeypatch.setenv("LOGGING_LEVEL", logging_level)
    monkeypatch.setenv("LOGGING_FMT", "test-fmt")
    monkeypatch.setenv("LOGGING_DATEFMT", "test-datefmt")

    sut = load_logging_settings()

    assert sut.level == logging_level
    assert sut.fmt == "test-fmt"
    assert sut.datefmt == "test-datefmt"


def test_load_fastapi_settings_reads_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FASTAPI_DEBUG", "1")
    monkeypatch.setenv("FASTAPI_DOCS_URL", "/test-docs")
    monkeypatch.setenv("FASTAPI_REDOC_URL", "/test-redoc")
    monkeypatch.setenv("FASTAPI_OPENAPI_URL", "/test-openapi.json")

    sut = load_fastapi_settings()

    assert sut.debug is True
    assert sut.docs_url == "/test-docs"
    assert sut.redoc_url == "/test-redoc"
    assert sut.openapi_url == "/test-openapi.json"

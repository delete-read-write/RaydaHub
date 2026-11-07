import logging
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

import uvicorn
from fastapi import FastAPI

from raydahub.bootstrap.setup import setup_logging
from raydahub.core.config.loader import (
    load_app_settings,
    load_fastapi_settings,
    load_logging_settings,
)

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Callable
    from contextlib import AbstractAsyncContextManager

    from raydahub.core.config.settings import AppSettings, FastAPISettings, LoggingSettings

logger = logging.getLogger(__name__)


def make_lifespan() -> Callable[[FastAPI], AbstractAsyncContextManager[None]]:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        logger.info("Starting %s", app.title)
        yield
        logger.info("Stopping %s", app.title)

    return lifespan


def make_app(
    *,
    app_settings: AppSettings | None = None,
    logging_settings: LoggingSettings | None = None,
    fastapi_settings: FastAPISettings | None = None,
) -> FastAPI:
    logging_settings = logging_settings or load_logging_settings()

    setup_logging(settings=logging_settings)

    app_settings = app_settings or load_app_settings()
    fastapi_settings = fastapi_settings or load_fastapi_settings()

    app = FastAPI(
        debug=fastapi_settings.debug,
        title=app_settings.service_name,
        version=app_settings.service_version,
        lifespan=make_lifespan(),
        openapi_url=fastapi_settings.openapi_url,
        docs_url=fastapi_settings.docs_url,
        redoc_url=fastapi_settings.redoc_url,
    )

    app.state.app_settings = app_settings
    app.state.logging_settings = logging_settings
    app.state.fastapi_settings = fastapi_settings

    return app


def main() -> None:
    uvicorn.run(app=make_app())


if __name__ == "__main__":
    main()

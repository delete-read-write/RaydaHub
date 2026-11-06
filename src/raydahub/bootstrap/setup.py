import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from raydahub.core.config.settings import LoggingSettings

logger = logging.getLogger(__name__)


def setup_logging(*, settings: LoggingSettings) -> None:
    logging.basicConfig(
        format=settings.fmt,
        datefmt=settings.datefmt,
        level=settings.level,
        force=True,
    )
    logger.info("Logging is set up!")

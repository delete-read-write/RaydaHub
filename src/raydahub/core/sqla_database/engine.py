from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

if TYPE_CHECKING:
    from raydahub.core.config.settings import PostgresSettings, SQLASettings


def make_sqla_async_engine(
    *,
    postgres_settings: PostgresSettings,
    sqla_settings: SQLASettings,
) -> AsyncEngine:
    return create_async_engine(
        url=postgres_settings.dsn,
        echo=sqla_settings.echo,
        echo_pool=sqla_settings.echo_pool,
        pool_size=sqla_settings.pool_size,
        max_overflow=sqla_settings.max_overflow,
        connect_args={"connect_timeout": sqla_settings.connect_timeout_s},
    )

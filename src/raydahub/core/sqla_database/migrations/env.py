import asyncio
from typing import TYPE_CHECKING

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

import raydahub.modules.session.sqla_models
import raydahub.modules.user.sqla_models  # noqa: F401
from raydahub.bootstrap.setup import setup_logging
from raydahub.core.config.loader import load_logging_settings, load_postgres_settings
from raydahub.core.sqla_database.base import Base

if TYPE_CHECKING:
    from sqlalchemy.engine import Connection

target_metadata = Base.metadata


def run_migrations_offline(*, url: str) -> None:
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online(*, url: str) -> None:
    engine = create_async_engine(url, poolclass=pool.NullPool)

    try:
        async with engine.connect() as connection:
            await connection.run_sync(do_run_migrations)
    finally:
        await engine.dispose()


def main() -> None:
    setup_logging(settings=load_logging_settings())
    url = load_postgres_settings().dsn

    if context.is_offline_mode():
        run_migrations_offline(url=url)
    else:
        asyncio.run(run_migrations_online(url=url))


main()

from typing import TYPE_CHECKING

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from raydahub.core.config.loader import load_postgres_settings, load_sqla_settings
from raydahub.core.sqla_database.base import Base
from raydahub.core.sqla_database.engine import make_sqla_async_engine

if TYPE_CHECKING:
    from collections.abc import AsyncIterator


@pytest.fixture(autouse=True)
def test_database_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("POSTGRES_USER", "test")
    monkeypatch.setenv("POSTGRES_PASSWORD", "test")
    monkeypatch.setenv("POSTGRES_HOST", "localhost")
    monkeypatch.setenv("POSTGRES_PORT", "15432")
    monkeypatch.setenv("POSTGRES_DB", "test")


@pytest.fixture
async def sqla_async_session() -> AsyncIterator[AsyncSession]:
    engine = make_sqla_async_engine(
        postgres_settings=load_postgres_settings(),
        sqla_settings=load_sqla_settings(),
    )
    try:
        async with engine.connect() as connection:
            transaction = await connection.begin()
            await connection.run_sync(Base.metadata.create_all)

            async with AsyncSession(
                bind=connection,
                join_transaction_mode="create_savepoint",
            ) as session:
                yield session

            await transaction.rollback()
    finally:
        await engine.dispose()

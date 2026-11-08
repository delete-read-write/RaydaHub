from sqlalchemy import text

from raydahub.core.config.loader import load_postgres_settings, load_sqla_settings
from raydahub.core.sqla_database.engine import make_sqla_async_engine


async def test_engine_connects_to_database() -> None:
    engine = make_sqla_async_engine(
        postgres_settings=load_postgres_settings(),
        sqla_settings=load_sqla_settings(),
    )
    try:
        async with engine.connect() as connection:
            result = await connection.execute(text("SELECT 1"))

        assert result.scalar_one() == 1
    finally:
        await engine.dispose()

from typing import TYPE_CHECKING

import pytest
from alembic import command
from alembic.config import Config

if TYPE_CHECKING:
    from collections.abc import Iterator


@pytest.fixture
def alembic_config(pytestconfig: pytest.Config) -> Iterator[Config]:
    config = Config(toml_file=str(pytestconfig.rootpath / "pyproject.toml"))
    yield config
    command.downgrade(config, "base")


def test_migrations_upgrade_and_downgrade(alembic_config: Config) -> None:
    command.upgrade(alembic_config, "head")
    command.downgrade(alembic_config, "base")
    command.upgrade(alembic_config, "head")


def test_migrations_match_models(alembic_config: Config) -> None:
    command.upgrade(alembic_config, "head")
    command.check(alembic_config)

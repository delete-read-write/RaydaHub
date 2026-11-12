from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest

INFRA_DIR = Path(__file__).parent / "integration" / "with_infra"


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--infra", action="store_true", help="run only tests that need infrastructure")
    parser.addoption("--all", action="store_true", help="run all tests")


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if config.getoption("--all"):
        return

    run_infra = config.getoption("--infra")
    selected: list[pytest.Item] = []
    deselected: list[pytest.Item] = []
    for item in items:
        if item.path.is_relative_to(INFRA_DIR) == run_infra:
            selected.append(item)
        else:
            deselected.append(item)

    if deselected:
        config.hook.pytest_deselected(items=deselected)
        items[:] = selected

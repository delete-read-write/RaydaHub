import uuid
from dataclasses import dataclass

from raydahub.core.entities import Entity


@dataclass(slots=True, kw_only=True, eq=False)
class FirstEntity(Entity[uuid.UUID]):
    pass


@dataclass(slots=True, kw_only=True, eq=False)
class SecondEntity(Entity[uuid.UUID]):
    pass


def test_entities_of_different_types_with_same_id_are_not_equal() -> None:
    entity_id = uuid.uuid7()

    assert FirstEntity(id=entity_id) != SecondEntity(id=entity_id)

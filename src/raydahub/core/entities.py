from dataclasses import dataclass
from typing import override


@dataclass(slots=True, kw_only=True, eq=False)
class Entity[T]:
    id: T

    @override
    def __eq__(self, other: object) -> bool:
        return type(other) is type(self) and self.id == other.id

    @override
    def __hash__(self) -> int:
        return hash(self.id)

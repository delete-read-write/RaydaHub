import hashlib
from dataclasses import dataclass, field

from raydahub.core.value_objects import ValueObject


@dataclass(frozen=True, slots=True)
class SessionToken(ValueObject[str]):
    value: str = field(repr=False)

    def hash(self) -> SessionTokenHash:
        return SessionTokenHash(hashlib.sha256(self.value.encode()).hexdigest())


@dataclass(frozen=True, slots=True)
class SessionTokenHash(ValueObject[str]):
    pass

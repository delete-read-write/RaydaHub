import hashlib
from dataclasses import dataclass


@dataclass(frozen=True, slots=True, repr=False)
class SessionToken:
    value: str

    def hash(self) -> SessionTokenHash:
        return SessionTokenHash(hashlib.sha256(self.value.encode()).hexdigest())


@dataclass(frozen=True, slots=True)
class SessionTokenHash:
    value: str

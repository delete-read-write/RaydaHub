from dataclasses import dataclass, field
from typing import ClassVar

from raydahub.core.value_objects import ValueObject


@dataclass(frozen=True, slots=True)
class Email(ValueObject[str]):
    EMAIL_MAX_LENGTH: ClassVar[int] = 320

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()
        local, _, domain = normalized.partition("@")

        if (
            len(normalized) > self.EMAIL_MAX_LENGTH
            or not local
            or "@" in domain
            or "." not in domain
        ):
            msg = f"Invalid email: {self.value!r}"
            raise ValueError(msg)

        object.__setattr__(self, "value", normalized)


@dataclass(frozen=True, slots=True)
class HashedPassword(ValueObject[str]):
    value: str = field(repr=False)

import datetime as dt
from dataclasses import dataclass

from raydahub.core.exception import BusinessTypeError


@dataclass(frozen=True, slots=True)
class ValueObject[T]:
    value: T


@dataclass(frozen=True, slots=True, order=True)
class DateTime(ValueObject[dt.datetime]):
    def __post_init__(self) -> None:
        if self.value.tzinfo is None:
            raise BusinessTypeError(f"Naive datetime: {self.value!r}")

        object.__setattr__(self, "value", self.value.astimezone(dt.UTC))

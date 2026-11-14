import datetime as dt
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValueObject[T]:
    value: T


@dataclass(frozen=True, slots=True, order=True)
class DateTime(ValueObject[dt.datetime]):
    def __post_init__(self) -> None:
        if self.value.tzinfo is None:
            raise ValueError(f"Naive datetime: {self.value!r}")

        object.__setattr__(self, "value", self.value.astimezone(dt.UTC))

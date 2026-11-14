from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValueObject[T]:
    value: T

from typing import ClassVar


class BaseError(Exception):
    default_message: ClassVar[str | None] = None

    def __init__(self, message: str | None = None) -> None:
        msg = message if message is not None else self.default_message
        if msg is None:
            super().__init__()
        else:
            super().__init__(msg)


class BusinessTypeError(BaseError):
    """Invalid value passed to a value object."""

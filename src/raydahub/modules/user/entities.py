from dataclasses import dataclass
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    from raydahub.core.value_objects import DateTime
    from raydahub.modules.user.types_ import UserId
    from raydahub.modules.user.value_objects import Email, HashedPassword


@dataclass(slots=True, kw_only=True, eq=False)
class UserEntity:
    id: UserId
    email: Email
    hashed_password: HashedPassword
    is_active: bool
    created_at: DateTime

    @override
    def __eq__(self, other: object) -> bool:
        return isinstance(other, UserEntity) and self.id == other.id

    @override
    def __hash__(self) -> int:
        return hash(self.id)

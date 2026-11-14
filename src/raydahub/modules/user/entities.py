from dataclasses import dataclass
from typing import TYPE_CHECKING

from raydahub.core.entities import Entity
from raydahub.modules.user.types_ import UserId

if TYPE_CHECKING:
    from raydahub.core.value_objects import DateTime
    from raydahub.modules.user.value_objects import Email, HashedPassword


@dataclass(slots=True, kw_only=True, eq=False)
class UserEntity(Entity[UserId]):
    email: Email
    hashed_password: HashedPassword
    is_active: bool
    created_at: DateTime

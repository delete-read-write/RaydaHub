from dataclasses import dataclass
from typing import TYPE_CHECKING

from raydahub.core.entities import Entity
from raydahub.modules.session.types_ import SessionId

if TYPE_CHECKING:
    from raydahub.core.value_objects import DateTime
    from raydahub.modules.session.value_objects import SessionTokenHash
    from raydahub.modules.user.types_ import UserId


@dataclass(slots=True, kw_only=True, eq=False)
class SessionEntity(Entity[SessionId]):
    user_id: UserId
    token_hash: SessionTokenHash
    created_at: DateTime
    expires_at: DateTime

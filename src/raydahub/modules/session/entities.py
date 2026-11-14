from dataclasses import dataclass
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    from raydahub.core.value_objects import DateTime
    from raydahub.modules.session.types_ import SessionId
    from raydahub.modules.session.value_objects import SessionTokenHash
    from raydahub.modules.user.types_ import UserId


@dataclass(slots=True, kw_only=True, eq=False)
class SessionEntity:
    id: SessionId
    user_id: UserId
    token_hash: SessionTokenHash
    created_at: DateTime
    expires_at: DateTime

    @override
    def __eq__(self, other: object) -> bool:
        return isinstance(other, SessionEntity) and self.id == other.id

    @override
    def __hash__(self) -> int:
        return hash(self.id)

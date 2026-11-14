from dataclasses import dataclass
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    import datetime as dt

    from raydahub.modules.session.types_ import SessionId
    from raydahub.modules.session.value_objects import SessionTokenHash
    from raydahub.modules.user.types_ import UserId


@dataclass(slots=True, kw_only=True, eq=False)
class SessionEntity:
    id: SessionId
    user_id: UserId
    token_hash: SessionTokenHash
    created_at: dt.datetime
    expires_at: dt.datetime

    @override
    def __eq__(self, other: object) -> bool:
        return isinstance(other, SessionEntity) and self.id == other.id

    @override
    def __hash__(self) -> int:
        return hash(self.id)

import datetime as dt
from typing import TYPE_CHECKING

from raydahub.modules.session.entities import SessionEntity
from raydahub.modules.session.factory import make_session_id, make_session_token
from raydahub.modules.user.factory import make_user_id

if TYPE_CHECKING:
    from raydahub.modules.session.types_ import SessionId


def make_session_entity(*, session_id: SessionId) -> SessionEntity:
    now = dt.datetime.now(dt.UTC)
    return SessionEntity(
        id=session_id,
        user_id=make_user_id(),
        token_hash=make_session_token().hash(),
        created_at=now,
        expires_at=now + dt.timedelta(days=30),
    )


def test_session_entities_with_same_id_are_equal() -> None:
    session_id = make_session_id()
    sut = make_session_entity(session_id=session_id)
    other = make_session_entity(session_id=session_id)

    assert sut == other
    assert len({sut, other}) == 1


def test_session_entities_with_different_ids_are_not_equal() -> None:
    sut = make_session_entity(session_id=make_session_id())
    other = make_session_entity(session_id=make_session_id())

    assert sut != other

import dataclasses
import datetime as dt
from typing import TYPE_CHECKING

import pytest
from sqlalchemy.exc import IntegrityError

from raydahub.core.factory import make_utc_now
from raydahub.core.value_objects import DateTime
from raydahub.modules.session.entities import SessionEntity
from raydahub.modules.session.factory import make_session_id, make_session_token
from raydahub.modules.session.sqla_repository import SQLASessionRepository
from raydahub.modules.user.entities import UserEntity
from raydahub.modules.user.factory import make_user_id
from raydahub.modules.user.sqla_repository import SQLAUserRepository
from raydahub.modules.user.value_objects import Email, HashedPassword

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from raydahub.modules.session.value_objects import SessionTokenHash
    from raydahub.modules.user.types_ import UserId


def make_session_entity(
    *,
    user_id: UserId,
    token_hash: SessionTokenHash | None = None,
) -> SessionEntity:
    now = make_utc_now()
    return SessionEntity(
        id=make_session_id(),
        user_id=user_id,
        token_hash=token_hash or make_session_token().hash(),
        created_at=now,
        expires_at=DateTime(now.value + dt.timedelta(days=30)),
    )


@pytest.fixture
def repository(sqla_async_session: AsyncSession) -> SQLASessionRepository:
    return SQLASessionRepository(sqla_async_session)


@pytest.fixture
def user_repository(sqla_async_session: AsyncSession) -> SQLAUserRepository:
    return SQLAUserRepository(sqla_async_session)


@pytest.fixture
async def user(
    sqla_async_session: AsyncSession,
    user_repository: SQLAUserRepository,
) -> UserEntity:
    user = UserEntity(
        id=make_user_id(),
        email=Email("user@example.com"),
        hashed_password=HashedPassword("hash"),
        is_active=True,
        created_at=make_utc_now(),
    )
    await user_repository.add(user)
    await sqla_async_session.flush()
    return user


async def test_get_by_token_hash_returns_added_session(
    sqla_async_session: AsyncSession,
    repository: SQLASessionRepository,
    user: UserEntity,
) -> None:
    session = make_session_entity(user_id=user.id)
    await repository.add(session)
    await sqla_async_session.flush()
    sqla_async_session.expunge_all()

    sut = await repository.get_by_token_hash(session.token_hash)

    assert sut is not None
    assert dataclasses.asdict(sut) == dataclasses.asdict(session)


async def test_add_rejects_duplicate_token_hash(
    sqla_async_session: AsyncSession,
    repository: SQLASessionRepository,
    user: UserEntity,
) -> None:
    token_hash = make_session_token().hash()
    await repository.add(make_session_entity(user_id=user.id, token_hash=token_hash))
    await repository.add(make_session_entity(user_id=user.id, token_hash=token_hash))

    with pytest.raises(IntegrityError, match="uq_sessions_token_hash"):
        await sqla_async_session.flush()


async def test_add_rejects_missing_user(
    sqla_async_session: AsyncSession,
    repository: SQLASessionRepository,
) -> None:
    await repository.add(make_session_entity(user_id=make_user_id()))

    with pytest.raises(IntegrityError, match="fk_sessions_user_id_users"):
        await sqla_async_session.flush()


async def test_delete_removes_session(
    sqla_async_session: AsyncSession,
    repository: SQLASessionRepository,
    user: UserEntity,
) -> None:
    session = make_session_entity(user_id=user.id)
    await repository.add(session)
    await sqla_async_session.flush()
    sqla_async_session.expunge_all()

    await repository.delete(session)
    await sqla_async_session.flush()

    assert await repository.get_by_token_hash(session.token_hash) is None


async def test_delete_by_user_id_removes_only_user_sessions(
    sqla_async_session: AsyncSession,
    repository: SQLASessionRepository,
    user_repository: SQLAUserRepository,
    user: UserEntity,
) -> None:
    other_user = dataclasses.replace(user, id=make_user_id(), email=Email("other@example.com"))
    await user_repository.add(other_user)
    sessions = [make_session_entity(user_id=user.id), make_session_entity(user_id=user.id)]
    other_session = make_session_entity(user_id=other_user.id)
    for session in [*sessions, other_session]:
        await repository.add(session)
    await sqla_async_session.flush()

    await repository.delete_by_user_id(user.id)

    for session in sessions:
        assert await repository.get_by_token_hash(session.token_hash) is None
    assert await repository.get_by_token_hash(other_session.token_hash) is not None


async def test_deleting_user_removes_user_sessions(
    sqla_async_session: AsyncSession,
    repository: SQLASessionRepository,
    user_repository: SQLAUserRepository,
    user: UserEntity,
) -> None:
    session = make_session_entity(user_id=user.id)
    await repository.add(session)
    await sqla_async_session.flush()

    await user_repository.delete(user)
    await sqla_async_session.flush()
    sqla_async_session.expunge_all()

    assert await repository.get_by_token_hash(session.token_hash) is None


async def test_delete_ignores_missing_session(
    sqla_async_session: AsyncSession,
    repository: SQLASessionRepository,
    user: UserEntity,
) -> None:
    session = make_session_entity(user_id=user.id)
    await repository.add(session)
    await sqla_async_session.flush()

    await repository.delete(make_session_entity(user_id=user.id))
    await sqla_async_session.flush()

    assert await repository.get_by_token_hash(session.token_hash) is not None

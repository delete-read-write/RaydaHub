import dataclasses
from typing import TYPE_CHECKING

import pytest
from sqlalchemy.exc import IntegrityError

from raydahub.core.factory import make_utc_now
from raydahub.modules.user.entities import UserEntity
from raydahub.modules.user.factory import make_user_id
from raydahub.modules.user.sqla_repository import SQLAUserRepository
from raydahub.modules.user.value_objects import Email, HashedPassword

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


def make_user_entity(*, email: str = "user@example.com") -> UserEntity:
    return UserEntity(
        id=make_user_id(),
        email=Email(email),
        hashed_password=HashedPassword("hash"),
        is_active=True,
        created_at=make_utc_now(),
    )


@pytest.fixture
def repository(sqla_async_session: AsyncSession) -> SQLAUserRepository:
    return SQLAUserRepository(sqla_async_session)


async def test_get_by_id_returns_added_user(
    sqla_async_session: AsyncSession,
    repository: SQLAUserRepository,
) -> None:
    user = make_user_entity()
    await repository.add(user)
    await sqla_async_session.flush()
    sqla_async_session.expunge_all()

    sut = await repository.get_by_id(user.id)

    assert sut is not None
    assert dataclasses.asdict(sut) == dataclasses.asdict(user)


async def test_get_by_email_returns_added_user(
    sqla_async_session: AsyncSession,
    repository: SQLAUserRepository,
) -> None:
    user = make_user_entity(email="User@Example.com")
    await repository.add(user)
    await sqla_async_session.flush()
    sqla_async_session.expunge_all()

    sut = await repository.get_by_email(Email("user@example.com"))

    assert sut is not None
    assert dataclasses.asdict(sut) == dataclasses.asdict(user)


async def test_add_rejects_duplicate_email(
    sqla_async_session: AsyncSession,
    repository: SQLAUserRepository,
) -> None:
    await repository.add(make_user_entity())
    await repository.add(make_user_entity())

    with pytest.raises(IntegrityError, match="uq_users_email"):
        await sqla_async_session.flush()


async def test_delete_removes_user(
    sqla_async_session: AsyncSession,
    repository: SQLAUserRepository,
) -> None:
    user = make_user_entity()
    await repository.add(user)
    await sqla_async_session.flush()
    sqla_async_session.expunge_all()

    await repository.delete(user)
    await sqla_async_session.flush()

    assert await repository.get_by_id(user.id) is None


async def test_delete_ignores_missing_user(
    sqla_async_session: AsyncSession,
    repository: SQLAUserRepository,
) -> None:
    user = make_user_entity()
    await repository.add(user)
    await sqla_async_session.flush()

    await repository.delete(make_user_entity(email="missing@example.com"))
    await sqla_async_session.flush()

    assert await repository.get_by_id(user.id) is not None

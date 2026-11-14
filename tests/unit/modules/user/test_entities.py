import datetime as dt
from typing import TYPE_CHECKING

from raydahub.modules.user.entities import UserEntity
from raydahub.modules.user.factory import make_user_id
from raydahub.modules.user.value_objects import Email, HashedPassword

if TYPE_CHECKING:
    from raydahub.modules.user.types_ import UserId


def make_user_entity(*, user_id: UserId, email: str = "user@example.com") -> UserEntity:
    return UserEntity(
        id=user_id,
        email=Email(email),
        hashed_password=HashedPassword("hash"),
        is_active=True,
        created_at=dt.datetime.now(dt.UTC),
    )


def test_user_entities_with_same_id_are_equal() -> None:
    user_id = make_user_id()
    sut = make_user_entity(user_id=user_id)
    other = make_user_entity(user_id=user_id, email="other@example.com")

    assert sut == other
    assert len({sut, other}) == 1


def test_user_entities_with_different_ids_are_not_equal() -> None:
    sut = make_user_entity(user_id=make_user_id())
    other = make_user_entity(user_id=make_user_id())

    assert sut != other

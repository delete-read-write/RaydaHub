from typing import TYPE_CHECKING

from sqlalchemy import select

from raydahub.modules.user.entities import UserEntity
from raydahub.modules.user.sqla_models import UserModel
from raydahub.modules.user.types_ import UserId
from raydahub.modules.user.value_objects import Email, HashedPassword

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class SQLAUserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, entity: UserEntity) -> None:
        self._session.add(self._to_model(entity))

    async def get_by_id(self, user_id: UserId) -> UserEntity | None:
        model = await self._session.get(UserModel, user_id)
        return None if model is None else self._to_entity(model)

    async def get_by_email(self, email: Email) -> UserEntity | None:
        model = await self._session.scalar(
            select(UserModel).where(UserModel.email == email.value),
        )
        return None if model is None else self._to_entity(model)

    async def delete(self, entity: UserEntity) -> None:
        model = await self._session.get(UserModel, entity.id)
        if model is not None:
            await self._session.delete(model)

    @staticmethod
    def _to_model(entity: UserEntity) -> UserModel:
        return UserModel(
            id=entity.id,
            email=entity.email.value,
            hashed_password=entity.hashed_password.value,
            is_active=entity.is_active,
            created_at=entity.created_at,
        )

    @staticmethod
    def _to_entity(model: UserModel) -> UserEntity:
        return UserEntity(
            id=UserId(model.id),
            email=Email(model.email),
            hashed_password=HashedPassword(model.hashed_password),
            is_active=model.is_active,
            created_at=model.created_at,
        )

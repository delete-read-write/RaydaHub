from typing import TYPE_CHECKING

from sqlalchemy import delete, select

from raydahub.modules.session.entities import SessionEntity
from raydahub.modules.session.sqla_models import SessionModel
from raydahub.modules.session.types_ import SessionId
from raydahub.modules.session.value_objects import SessionTokenHash
from raydahub.modules.user.types_ import UserId

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class SQLASessionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, entity: SessionEntity) -> None:
        self._session.add(self._to_model(entity))

    async def get_by_token_hash(self, token_hash: SessionTokenHash) -> SessionEntity | None:
        model = await self._session.scalar(
            select(SessionModel).where(SessionModel.token_hash == token_hash.value),
        )
        return None if model is None else self._to_entity(model)

    async def delete(self, entity: SessionEntity) -> None:
        model = await self._session.get(SessionModel, entity.id)
        if model is not None:
            await self._session.delete(model)

    async def delete_by_user_id(self, user_id: UserId) -> None:
        await self._session.execute(
            delete(SessionModel).where(SessionModel.user_id == user_id),
        )

    @staticmethod
    def _to_model(entity: SessionEntity) -> SessionModel:
        return SessionModel(
            id=entity.id,
            user_id=entity.user_id,
            token_hash=entity.token_hash.value,
            created_at=entity.created_at,
            expires_at=entity.expires_at,
        )

    @staticmethod
    def _to_entity(model: SessionModel) -> SessionEntity:
        return SessionEntity(
            id=SessionId(model.id),
            user_id=UserId(model.user_id),
            token_hash=SessionTokenHash(model.token_hash),
            created_at=model.created_at,
            expires_at=model.expires_at,
        )

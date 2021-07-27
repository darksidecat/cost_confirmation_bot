from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.access_levels.interfaces.repo import IAccessLevelRepo
from app.domain.access_levels.interfaces.uow import IAccessLevelUoW
from app.domain.common.interfaces.uow import IUoW
from app.domain.user.interfaces.repo import IUserRepo
from app.domain.user.interfaces.uow import IUserUoW
from app.infrastructure.database.exception_mapper import exception_mapper


class SQLAlchemyBaseUoW(IUoW):
    def __init__(self, session: AsyncSession):
        self._session = session

    @exception_mapper
    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()


class SQLAlchemyUoW(SQLAlchemyBaseUoW, IUserUoW, IAccessLevelUoW):
    user: IUserRepo
    access_level: IAccessLevelRepo

    def __init__(
        self,
        session: AsyncSession,
        user_repo: Type[IUserRepo],
        access_level_repo: Type[IAccessLevelRepo],
    ):
        self.user = user_repo(session)
        self.access_level = access_level_repo(session)
        super().__init__(session)

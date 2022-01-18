from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.access_levels.interfaces.persistence import IAccessLevelReader
from app.domain.access_levels.interfaces.uow import IAccessLevelUoW
from app.domain.common.interfaces.uow import IUoW
from app.domain.user.interfaces.persistence import IUserReader, IUserRepo
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
    user_reader = IUserReader
    access_level_reader: IAccessLevelReader

    def __init__(
        self,
        session: AsyncSession,
        user_repo: Type[IUserRepo],
        user_reader: Type[IUserReader],
        access_level_reader: Type[IAccessLevelReader],
    ):
        self.user = user_repo(session)
        self.user_reader = user_reader(session)
        self.access_level_reader = access_level_reader(session)
        super().__init__(session)

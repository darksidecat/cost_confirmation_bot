from typing import List

from pydantic import parse_obj_as
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.domain.access_levels.interfaces.repo import IAccessLevelRepo
from app.domain.access_levels.models.access_level import AccessLevel
from app.domain.user.exceptions.user import UserNotExists
from app.infrastructure.database.exception_mapper import exception_mapper
from app.infrastructure.database.models import AccessLevelEntry, TelegramUserEntry
from app.infrastructure.database.repositories.repo import SQLAlchemyRepo


class AccessLevelRepo(SQLAlchemyRepo, IAccessLevelRepo):
    @exception_mapper
    async def all_access_levels(self) -> List[AccessLevel]:
        query = select(AccessLevelEntry).options(selectinload(AccessLevelEntry.users))
        result = await self.session.execute(query)
        access_levels = result.scalars().all()

        return parse_obj_as(List[AccessLevel], access_levels)

    @exception_mapper
    async def user_access_levels(self, user_id: int) -> List[AccessLevel]:
        user = await self.session.get(TelegramUserEntry, user_id)

        if not user:
            raise UserNotExists

        return parse_obj_as(List[AccessLevel], user.access_levels)

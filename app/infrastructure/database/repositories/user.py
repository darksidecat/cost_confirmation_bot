import logging
from typing import List

from pydantic import parse_obj_as
from sqlalchemy import delete, select

from app.domain.access_levels.entities.access_level import AccessLevel
from app.domain.access_levels.exceptions.access_levels import AccessLevelNotExist
from app.domain.user.entities.user import User
from app.domain.user.exceptions.user import UserNotExist
from app.domain.user.interfaces.repo import IUserRepo
from app.infrastructure.database.exception_mapper import exception_mapper
from app.infrastructure.database.models import AccessLevelEntry, TelegramUserEntry
from app.infrastructure.database.repositories.repo import SQLAlchemyRepo

logger = logging.getLogger(__name__)


class UserRepo(SQLAlchemyRepo, IUserRepo):
    @exception_mapper
    async def _assign_levels(
        self, user: TelegramUserEntry, access_levels: list[AccessLevel]
    ):
        levels = []
        for access_level in access_levels:
            l = await self.session.get(AccessLevelEntry, access_level.id)
            if l is not None:
                levels.append(l)
            else:
                raise AccessLevelNotExist(
                    f"Access level with id {access_level.id} not found"
                )  # Todo
        user.access_levels = levels
        return user

    @exception_mapper
    async def add_user(self, user: User) -> User:
        new_user = TelegramUserEntry(id=user.id, name=user.name)
        new_user = await self._assign_levels(new_user, user.access_levels)

        self.session.add(new_user)

        return User.from_orm(new_user)

    @exception_mapper
    async def all_users(self) -> List[User]:
        query = select(TelegramUserEntry)

        result = await self.session.execute(query)
        users = result.scalars().all()

        return parse_obj_as(List[User], users)

    @exception_mapper
    async def user_by_id(self, user_id: int) -> User:
        user = await self.session.get(TelegramUserEntry, user_id)
        if user:
            return User.from_orm(user)
        else:
            raise UserNotExist

    @exception_mapper
    async def delete_user(self, user_id: int) -> None:
        user = await self.session.get(TelegramUserEntry, user_id)
        if not user:
            raise UserNotExist

        await self.session.delete(user)
        await self.session.flush()

    @exception_mapper
    async def edit_user(self, user_id: int, user: User) -> User:
        db_user = await self.session.get(TelegramUserEntry, user_id)

        if not db_user:
            raise UserNotExist

        db_user.id = user.id
        db_user.name = user.name
        db_user = await self._assign_levels(db_user, user.access_levels)

        return User.from_orm(db_user)

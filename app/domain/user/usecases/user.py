import logging
from typing import List, Optional

from app.domain.access_levels.entities.access_level import id_to_access_levels
from app.domain.common.exceptions.repo import UniqueViolationError
from app.domain.user import dto
from app.domain.user.entities.user import User
from app.domain.user.exceptions.user import UserAlreadyExist, UserNotExist
from app.domain.user.interfaces.uow import IUserUoW

logger = logging.getLogger(__name__)


class GetUsers:
    def __init__(self, uow: IUserUoW) -> None:
        self.uow = uow

    async def __call__(self) -> List[User]:
        users = await self.uow.user.all_users()
        return users


class GetUser:
    def __init__(self, uow: IUserUoW) -> None:
        self.uow = uow

    async def __call__(self, user_id: int) -> Optional[User]:
        user = await self.uow.user.user_by_id(user_id)
        return user


class AddUser:
    def __init__(self, uow: IUserUoW) -> None:
        self.uow = uow

    async def __call__(self, user: dto.UserCreate) -> User:
        """
        Args:
            user: payload for user creation

        Returns:
            created user
        Raises:
            UserAlreadyExist - if user already exist
            AccessLevelNotExist - if user access level not exist
        """
        access_levels = id_to_access_levels(user.access_levels)

        user = User(
            id=user.id,
            name=user.name,
            access_levels=access_levels,
        )
        user = await self.uow.user.add_user(user=user)
        try:
            await self.uow.commit()
        except UniqueViolationError:
            raise UserAlreadyExist
        logger.info("User added: id=%s, %s", user.id, user)
        return user


class DeleteUser:
    def __init__(self, uow: IUserUoW) -> None:
        self.uow = uow

    async def __call__(self, user_id: int) -> None:
        """

        Args:
            user_id: user id for deleting

        Raises:
            UserNotExist - if user for deleting doesnt exist


        """
        await self.uow.user.delete_user(user_id)
        await self.uow.commit()
        logger.info("User deleted: id=%s,", user_id)


class PatchUser:
    def __init__(self, uow: IUserUoW) -> None:
        self.uow = uow

    async def __call__(self, new_user: dto.UserPatch) -> User:
        """
        Use for partially update User data

        Args:
            new_user: data for user editing

        Returns:
            edited user

        Raises:
            UserNotExist - if user for editing doesnt exist
            AccessLevelNotExist - if user access level not exist
            UserAlreadyExist - if already exist user with new user id
        """
        user = await self.uow.user.user_by_id(new_user.id)
        if not user:
            raise UserNotExist

        if new_user.user_data.id:
            user.id = new_user.user_data.id
        if new_user.user_data.name:
            user.name = new_user.user_data.name
        if new_user.user_data.access_levels:
            user.access_levels = id_to_access_levels(new_user.user_data.access_levels)

        try:
            updated_user = await self.uow.user.edit_user(user_id=new_user.id, user=user)
            await self.uow.commit()
        except UniqueViolationError:
            raise UserAlreadyExist
        logger.info("User edited: id=%s,", updated_user.id)
        return updated_user

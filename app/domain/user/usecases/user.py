import logging
from abc import ABC, abstractmethod
from typing import List, Any

from app.domain.access_levels.models.helper import id_to_access_levels
from app.domain.common.exceptions.base import AccessDenied
from app.domain.common.exceptions.repo import UniqueViolationError
from app.domain.policy.access_policy import AccessPolicy
from app.domain.user import dto
from app.domain.user.exceptions.user import UserAlreadyExists
from app.domain.user.interfaces.uow import IUserUoW
from app.domain.user.models.user import TelegramUser

logger = logging.getLogger(__name__)


class UserUseCase(ABC):
    def __init__(
            self,
            uow: IUserUoW,
    ) -> None:
        self.uow = uow

    @abstractmethod
    async def __call__(self, *args, **kwargs) -> Any:
        ...


class GetUsers(UserUseCase):
    async def __call__(self) -> List[dto.User]:
        users = await self.uow.user_reader.all_users()
        return users


class GetUser(UserUseCase):
    async def __call__(self, user_id: int, internal: bool = False) -> dto.User:
        """
        Args:
            user_id:

        Returns:
            user
        Raises:
            UserNotExists - if user doesnt exist
        """
        user = await self.uow.user_reader.user_by_id(user_id)
        return user


class AddUser(UserUseCase):
    async def __call__(self, user: dto.UserCreate) -> dto.User:
        """
        Args:
            user: payload for user creation

        Returns:
            created user
        Raises:
            UserAlreadyExists - if user already exist
            AccessLevelNotExist - if user access level not exist
        """
        user = TelegramUser(
            id=user.id,
            name=user.name,
            access_levels=id_to_access_levels(user.access_levels),
        )

        try:
            user = await self.uow.user.add_user(user=user)
            await self.uow.commit()
        except UniqueViolationError:
            await self.uow.rollback()
            raise UserAlreadyExists

        logger.info("User added: id=%s, %s", user.id, user)

        return dto.User.from_orm(user)


class DeleteUser(UserUseCase):
    async def __call__(self, user_id: int) -> None:
        """

        Args:
            user_id: user id for deleting

        Raises:
            UserNotExists - if user for deleting doesnt exist


        """
        await self.uow.user.delete_user(user_id)
        await self.uow.commit()

        logger.info("User deleted: id=%s,", user_id)


class PatchUser(UserUseCase):
    async def __call__(self, new_user: dto.UserPatch) -> dto.User:
        """
        Use for partially update User data

        Args:
            new_user: data for user editing

        Returns:
            edited user

        Raises:
            UserNotExists - if user for editing doesn't exist
            AccessLevelNotExist - if user access level not exist
            UserAlreadyExists - if already exist user with new user id
        """
        user = await self.uow.user.user_by_id(user_id=new_user.id)

        if new_user.user_data.id:
            user.id = new_user.user_data.id
        if new_user.user_data.name:
            user.name = new_user.user_data.name
        if new_user.user_data.access_levels:
            user.access_levels = id_to_access_levels(new_user.user_data.access_levels)
        try:
            updated_user = await self.uow.user.edit_user(user=user)
            await self.uow.commit()
        except UniqueViolationError:
            await self.uow.rollback()
            raise UserAlreadyExists

        logger.info("User edited: id=%s,", updated_user.id)

        return dto.User.from_orm(updated_user)


class UserService:
    def __init__(
            self,
            uow: IUserUoW,
            access_policy: AccessPolicy
    ) -> None:
        self.uow = uow
        self.access_policy = access_policy

    async def get_users(self) -> List[dto.User]:
        if not self.access_policy.read_user_policy():
            raise AccessDenied()
        return await GetUsers(uow=self.uow)()

    async def get_user(self, user_id: int, internal: bool = False) -> dto.User:
        if not (self.access_policy.read_user_policy() or internal):
            raise AccessDenied()
        return await GetUser(uow=self.uow)(user_id=user_id, internal=internal)

    async def add_user(self, user: dto.UserCreate) -> dto.User:
        if not self.access_policy.modify_user():
            raise AccessDenied()
        return await AddUser(uow=self.uow)(user=user)

    async def delete_user(self, user_id: int) -> None:
        if not self.access_policy.modify_user():
            raise AccessDenied()
        return await DeleteUser(uow=self.uow)(user_id=user_id)

    async def patch_user(self, new_user: dto.UserPatch) -> dto.User:
        if not self.access_policy.modify_user():
            raise AccessDenied()
        return await PatchUser(uow=self.uow)(new_user=new_user)

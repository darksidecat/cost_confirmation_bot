from typing import List

from app.domain.access_levels.dto.access_level import AccessLevel
from app.domain.access_levels.interfaces.uow import IAccessLevelUoW
from app.domain.common.exceptions.base import AccessDenied
from app.domain.policy.access_policy import AccessPolicy


class GetAccessLevels:
    def __init__(
            self,
            uow: IAccessLevelUoW,
            access_policy: AccessPolicy
    ) -> None:
        self.uow = uow
        self.access_policy = access_policy

    async def __call__(self) -> List[AccessLevel]:
        """

        Returns: List of AccessLevel

        """
        if not self.access_policy.read_access_levels():
            raise AccessDenied()
        return await self.uow.access_level_reader.all_access_levels()


class GetUserAccessLevels:
    def __init__(
            self,
            uow: IAccessLevelUoW,
            access_policy: AccessPolicy
    ) -> None:
        self.uow = uow
        self.access_policy = access_policy

    async def __call__(self, user_id: int) -> List[AccessLevel]:
        """
        Use for getting user access levels

        Args:
            user_id: user id

        Returns: List of AccessLevel

        Raises:
            UserNotExists - if user not exist

        """
        if not self.access_policy.read_access_levels():
            raise AccessDenied()
        return await self.uow.access_level_reader.user_access_levels(user_id)

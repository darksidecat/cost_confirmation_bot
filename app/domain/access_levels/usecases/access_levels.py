from typing import List

from app.domain.access_levels.entities.access_level import AccessLevel
from app.domain.access_levels.interfaces.uow import IAccessLevelUoW


class GetAccessLevels:
    def __init__(self, uow: IAccessLevelUoW) -> None:
        self.uow = uow

    async def __call__(self) -> List[AccessLevel]:
        """

        Returns: List of AccessLevel

        """
        return await self.uow.access_level.all_access_levels()


class GetUserAccessLevels:
    def __init__(self, uow: IAccessLevelUoW) -> None:
        self.uow = uow

    async def __call__(self, user_id: int) -> List[AccessLevel]:
        """
        Use for getting user access levels

        Args:
            user_id: user id

        Returns: List of AccessLevel

        Raises:
            UserNotExist - if user not exist

        """
        return await self.uow.access_level.user_access_levels(user_id)

from asyncio import Protocol

from app.domain.access_levels.entities.access_level import AccessLevel


class IAccessLevelRepo(Protocol):
    async def all_access_levels(self) -> list[AccessLevel]:
        ...

    async def user_access_levels(self, user_id: int) -> list[AccessLevel]:
        ...

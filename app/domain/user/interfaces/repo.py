from typing import List, Optional, Protocol

from app.domain.user.models.user import User


class IUserRepo(Protocol):
    async def add_user(self, user: User) -> User:
        ...

    async def all_users(self) -> List[User]:
        ...

    async def user_by_id(self, user_id: int) -> User:
        ...

    async def delete_user(self, user_id: int) -> None:
        ...

    async def edit_user(self, user_id: int, user: User) -> User:
        ...

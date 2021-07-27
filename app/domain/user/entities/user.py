from typing import Tuple

from pydantic import validator

from app.domain.access_levels.entities.access_level import AccessLevel, Levels
from app.domain.user.entities.base_user import BaseUser


class User(BaseUser):
    access_levels: Tuple[AccessLevel, ...]

    @validator("access_levels")
    def validate_access_levels(cls, v) -> Tuple[AccessLevel, ...]:
        if len(v) < 1:
            raise ValueError("User must have at least one access level")
        return tuple(set(v))

    @validator("access_levels")
    def validate_blocked_access_level(cls, v) -> Tuple[AccessLevel, ...]:
        if len(v) > 1 and Levels.BLOCKED.value in v:
            raise ValueError("Blocked user can have only that role")
        return v

    def block_user(self) -> None:
        self.access_levels = (Levels.BLOCKED.value,)

    @property
    def is_blocked(self) -> bool:
        return Levels.BLOCKED.value in self.access_levels

    @property
    def is_admin(self) -> bool:
        return Levels.ADMINISTRATOR.value in self.access_levels

from typing import List, Set

import attrs

from app.domain.access_levels.models.access_level import AccessLevel
from app.domain.access_levels.models.helper import Levels
from app.domain.common.models.entity import entity
from app.domain.user.exceptions.user import (
    BlockedUserWithOtherRole,
    UserWithNoAccessLevels,
)


def list_with_unique_values(access_levels: list):
    return list(set(access_levels))


@entity
class TelegramUser:
    id: int
    name: str
    access_levels: List[AccessLevel] = attrs.field(converter=list_with_unique_values)

    @access_levels.validator
    def validate_access_levels(self, attribute, value):
        if len(value) < 1:
            raise UserWithNoAccessLevels("User must have at least one access level")
        if len(value) > 1 and Levels.BLOCKED.value in value:
            raise BlockedUserWithOtherRole("Blocked user can have only that role")

    def block_user(self) -> None:
        self.access_levels = [
            Levels.BLOCKED.value,
        ]

    @property
    def is_blocked(self) -> bool:
        return Levels.BLOCKED.value in self.access_levels

    @property
    def is_admin(self) -> bool:
        return Levels.ADMINISTRATOR.value in self.access_levels

from collections.abc import Iterable
from enum import Enum, unique

from app.domain.access_levels.exceptions.access_levels import AccessLevelNotExist
from app.domain.common.models.value_object import ValueObject


@unique
class LevelName(Enum):
    BLOCKED = "BLOCKED"
    USER = "USER"
    ADMINISTRATOR = "ADMINISTRATOR"


class AccessLevel(ValueObject):
    id: int
    name: LevelName

    def __hash__(self):
        return hash((type(self), self.id))


class Levels(Enum):
    BLOCKED = AccessLevel(id=-1, name=LevelName.BLOCKED)
    ADMINISTRATOR = AccessLevel(id=1, name=LevelName.ADMINISTRATOR)
    USER = AccessLevel(id=2, name=LevelName.USER)


LEVELS_MAP = {level.value.id: level.value for level in Levels}


def id_to_access_levels(level_ids: Iterable[int]):
    if not set(level_ids).issubset(LEVELS_MAP):
        not_found_levels = set(level_ids).difference(LEVELS_MAP)
        raise AccessLevelNotExist(
            f"Access levels with ids: {not_found_levels} not found"
        )
    else:
        return tuple(LEVELS_MAP[level] for level in level_ids)

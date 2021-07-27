from app.domain.access_levels.interfaces.repo import IAccessLevelRepo
from app.domain.common.interfaces.uow import IUoW


class IAccessLevelUoW(IUoW):
    access_level: IAccessLevelRepo

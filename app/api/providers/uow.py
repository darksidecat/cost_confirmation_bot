from fastapi import Request

from app.domain.common.interfaces.uow import IUoW
from app.infrastructure.database.repositories.access_level import AccessLevelRepo
from app.infrastructure.database.repositories.user import UserRepo
from app.infrastructure.database.uow import SQLAlchemyUoW


def uow_provider(request: Request) -> IUoW:
    ...


def get_uow(request: Request) -> SQLAlchemyUoW:
    session = request.state.db_session
    uow = SQLAlchemyUoW(
        session,
        user_repo=UserRepo,
        access_level_repo=AccessLevelRepo,
    )
    request.state.uow = uow
    return request.state.uow

from fastapi import Request

from app.domain.common.interfaces.uow import IUoW
from app.infrastructure.database.repositories.access_level import AccessLevelReader
from app.infrastructure.database.repositories.user import UserReader, UserRepo
from app.infrastructure.database.uow import SQLAlchemyUoW


def uow_provider(request: Request) -> IUoW:
    ...


def get_uow(request: Request) -> SQLAlchemyUoW:
    session = request.state.db_session
    uow = SQLAlchemyUoW(
        session,
        user_repo=UserRepo,
        user_reader=UserReader,
        access_level_reader=AccessLevelReader,
    )
    request.state.uow = uow
    return request.state.uow

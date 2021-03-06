from fastapi import Depends, Request

from app.domain.access_levels.models.access_level import AccessLevel, LevelName
from app.domain.common.events.dispatcher import EventDispatcher
from app.domain.common.interfaces.uow import IUoW
from app.domain.user.access_policy import UserAccessPolicy
from app.domain.user.models.user import TelegramUser
from app.domain.user.usecases.user import UserService
from app.infrastructure.database.repositories.access_level import AccessLevelReader
from app.infrastructure.database.repositories.user import UserReader, UserRepo
from app.infrastructure.database.uow import SQLAlchemyUoW


def uow_provider(request: Request) -> IUoW:
    ...


def uow(request: Request) -> SQLAlchemyUoW:
    return SQLAlchemyUoW(
        request.state.db_session,
        user_repo=UserRepo,
        user_reader=UserReader,
        access_level_reader=AccessLevelReader,
    )


def user_provider() -> TelegramUser:
    ...


def user() -> TelegramUser:
    return TelegramUser(
        id=1,
        name="Test",
        access_levels=[AccessLevel(id=1, name=LevelName.ADMINISTRATOR)],
    )


def access_policy_provider(
    from_user: TelegramUser = Depends(user_provider),
) -> UserAccessPolicy:
    ...


def access_policy(from_user: TelegramUser = Depends(user_provider)) -> UserAccessPolicy:
    return UserAccessPolicy(user=from_user)


def user_service_provider(
    user_uow: TelegramUser = Depends(uow_provider),
    user_access_policy: UserAccessPolicy = Depends(access_policy_provider),
) -> UserService:
    ...


def event_dispatcher_provider() -> EventDispatcher:
    ...


def user_service(
    user_uow: SQLAlchemyUoW = Depends(uow_provider),
    user_access_policy: UserAccessPolicy = Depends(access_policy_provider),
    event_dicpatcher: EventDispatcher = Depends(event_dispatcher_provider),
) -> UserService:
    return UserService(
        uow=user_uow,
        access_policy=user_access_policy,
        event_dispatcher=event_dicpatcher,
    )

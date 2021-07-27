from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Update
from sqlalchemy.orm import sessionmaker

from app.infrastructure.database.repositories import AccessLevelRepo, UserRepo
from app.infrastructure.database.uow import SQLAlchemyUoW


class Database(BaseMiddleware):
    def __init__(self, sm: sessionmaker) -> None:
        self.Session = sm

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:

        async with self.Session() as session:
            data["session"] = session
            data["uow"] = SQLAlchemyUoW(
                session=session,
                user_repo=UserRepo,
                access_level_repo=AccessLevelRepo,
            )

            return await handler(event, data)

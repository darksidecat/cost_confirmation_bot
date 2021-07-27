from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Update

from app.domain.user.interfaces.uow import IUserUoW
from app.domain.user.usecases.user import GetUser


class UserDB(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:

        event_user_id = data["event_from_user"]
        if event_user_id:
            from_user_id = event_user_id.id

            uow: IUserUoW = data["uow"]
            get_user = GetUser(uow)
            user = await get_user(from_user_id)

            data["user"] = user

        return await handler(event, data)
